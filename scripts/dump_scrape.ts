import * as fs from "fs";
import * as path from "path";
import { getRepoRoot, GLOBAL_INBOX_DIR } from "./global_config";

const mechanisticRoot = getRepoRoot("mechanistic");
const targetFilesList = [
    path.join(mechanisticRoot, "src/dfmea_core/data/vault_s_synthesis_v29.json"),
    path.join(mechanisticRoot, "src/dfmea_core/data/vault_f_finance_v28.json"),
    path.join(mechanisticRoot, "src/dfmea_core/data/vault_l_legal_v28.json"),
    path.join(mechanisticRoot, "src/dfmea_core/data/vault_p_physics_v28.json"),
    path.join(mechanisticRoot, "src/components/dfmea/execute/MechanisticAndonViz.tsx"),
    path.join(mechanisticRoot, "src/components/dfmea/execute/DependencyLock.tsx"),
    path.join(mechanisticRoot, "src/components/dfmea/execute/DrawbridgeRoadmap.tsx"),
    path.join(mechanisticRoot, "src/components/dfmea/execute/FormalSow.tsx")
];

let payload = "--- MECHANISTIC LIVE DASHBOARD V29 EXPORT ---\n\n";

for (const file of targetFilesList) {
    if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, "utf-8");
        payload += `\n==============================================\n`;
        payload += `FILE: ${path.basename(file)}\n`;
        payload += `==============================================\n\n`;
        payload += `${content}\n`;
    } else {
        console.log(`[!] Missing File: ${file}`);
    }
}

const outPath = path.join(GLOBAL_INBOX_DIR, "mo_v29_dashboard_scrape.txt");
fs.writeFileSync(outPath, payload, "utf-8");
console.log(`[+] Dashboard data successfully scraped to: ${outPath}`);

export {};
