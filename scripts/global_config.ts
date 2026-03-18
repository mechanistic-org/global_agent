import path from 'path';
import fs from 'fs';
import dotenv from 'dotenv';

// Use __dirname to walk up the directory tree
// In standard CommonJS/Node environments, __dirname is the directory of the current file ('scripts')
// We resolve '..' to get to 'global_agent' root.
export const GLOBAL_AGENT_ROOT = path.resolve(__dirname, '..');

// Load local .env if it exists
const localEnvPath = path.join(GLOBAL_AGENT_ROOT, '.env');
if (fs.existsSync(localEnvPath)) {
    dotenv.config({ path: localEnvPath });
} else {
    console.warn(`⚠️ Warning: Global .env file not found at ${localEnvPath}`);
}

// Check for OS-level override, Local Repo override, then fallback to D:/Assets
const masterFallbackPath = 'D:/Assets/.env.swarm';
const masterEnvPath = process.env.SWARM_ENV_PATH || 
                      (fs.existsSync(localEnvPath) ? localEnvPath : masterFallbackPath);

if (fs.existsSync(masterEnvPath)) {
    dotenv.config({ path: masterEnvPath });
    console.log(`✅ Loaded Master Swarm Environment Cache from ${masterEnvPath}`);
} else {
    console.warn(`⚠️ Warning: Master Swarm Environment Cache not found at ${masterEnvPath}`);
}

// Sibling Repository Resolution
// We assume all repos sit in the same parent directory.
export const GITHUB_ROOT = path.resolve(GLOBAL_AGENT_ROOT, '..');

// Common Ecosystem Repositories
export const ERIKNORRIS_ROOT = path.join(GITHUB_ROOT, 'eriknorris');
export const MECHANISTIC_ROOT = path.join(GITHUB_ROOT, 'mechanistic');
export const MOOTMOAT_ROOT = path.join(GITHUB_ROOT, 'mootmoat');
export const PORTFOLIO_ROOT = path.join(GITHUB_ROOT, 'portfolio');

export function getRepoRoot(repoName: string): string {
    const repos: { [key: string]: string } = {
        'global_agent': GLOBAL_AGENT_ROOT,
        'eriknorris': ERIKNORRIS_ROOT,
        'mechanistic': MECHANISTIC_ROOT,
        'mootmoat': MOOTMOAT_ROOT,
        'portfolio': PORTFOLIO_ROOT
    };
    
    let repoPath = repos[repoName];
    if (!repoPath) {
        repoPath = path.join(GITHUB_ROOT, repoName);
    }
    
    if (!fs.existsSync(repoPath)) {
        throw new Error(`❌ Critical Error: Could not locate sibling repository '${repoName}' at ${repoPath}`);
    }
    
    return repoPath;
}

// Centralized utility paths
export const GLOBAL_INBOX_DIR = path.join(GLOBAL_AGENT_ROOT, '_inbox');

// Ensure directories exist
if (!fs.existsSync(GLOBAL_INBOX_DIR)) {
    fs.mkdirSync(GLOBAL_INBOX_DIR, { recursive: true });
}
const processedDir = path.join(GLOBAL_INBOX_DIR, 'processed');
if (!fs.existsSync(processedDir)) {
    fs.mkdirSync(processedDir, { recursive: true });
}
