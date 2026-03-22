#!/usr/bin/env node
/**
 * patcher.js — Sovereign OS AST Patcher (Pillar 2: Data Compressor)
 *
 * CLI:  node patcher.js <filepath> <target_selector> <json_payload_path>
 *
 * Parser strategy:
 *   - Frontmatter (ts block between ---): ts-morph
 *   - Template (Astro HTML body):         @astrojs/compiler
 *
 * Output: ONLY valid JSON to stdout. Never freeform strings.
 *         Caller (Python) parses stdout to feed the Pillar 3 circuit breaker.
 */

import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { parse } from "@astrojs/compiler";
import { is } from "@astrojs/compiler/utils";
import { Project } from "ts-morph";

// ─── Helpers ────────────────────────────────────────────────────────────────

function out(obj) {
  process.stdout.write(JSON.stringify(obj) + "\n");
}

function die(reason, detail = "") {
  out({ status: "error", reason, detail });
  process.exit(1);
}

// ─── CLI Argument Validation ─────────────────────────────────────────────────

const [, , rawFilepath, targetSelector, payloadPath] = process.argv;

if (!rawFilepath || !targetSelector || !payloadPath) {
  die("MISSING_ARGS", "Usage: node patcher.js <filepath> <target_selector> <json_payload_path>");
}

const filepath = path.resolve(rawFilepath);

// PATH SECURITY BOUNDARY — blocks rogue agents from patching OS files
const ALLOWED_PREFIX = path.resolve("D:\\GitHub").toLowerCase();
if (!filepath.toLowerCase().startsWith(ALLOWED_PREFIX)) {
  die("PATH_VIOLATION", `Target path '${filepath}' is outside the D:\\GitHub\\ boundary.`);
}

if (!fs.existsSync(filepath)) {
  die("FILE_NOT_FOUND", `No file at: ${filepath}`);
}

if (!fs.existsSync(payloadPath)) {
  die("PAYLOAD_NOT_FOUND", `No payload file at: ${payloadPath}`);
}

let payload;
try {
  payload = JSON.parse(fs.readFileSync(payloadPath, "utf8"));
} catch (e) {
  die("INVALID_PAYLOAD_JSON", e.message);
}

// ─── Read & Split the Astro File ─────────────────────────────────────────────

const rawSource = fs.readFileSync(filepath, "utf8");
const { data: frontmatterData, content: templateContent, matter: frontmatterRaw } = matter(rawSource);

// gray-matter gives us the frontmatter YAML data, but for .astro files the
// content between --- is TypeScript, not YAML. We work with the raw string.
const frontmatterMatch = rawSource.match(/^---\r?\n([\s\S]*?)\r?\n---/);
const frontmatterBlock = frontmatterMatch ? frontmatterMatch[1] : "";

// Everything after the closing ---
const templateBlock = rawSource.replace(/^---[\s\S]*?---\r?\n/, "");

// ─── Determine Which Engine to Use ──────────────────────────────────────────

const mode = payload.zone || "template"; // "frontmatter" | "template"
let modifiedLines = 0;
let newSource = rawSource;

// ─── Mode A: Frontmatter Mutation (ts-morph) ─────────────────────────────────

if (mode === "frontmatter") {
  const project = new Project({ useInMemoryFileSystem: true });
  const sourceFile = project.createSourceFile("__frontmatter__.ts", frontmatterBlock);

  if (payload.addImport) {
    const { moduleSpecifier, namedImport } = payload.addImport;
    const existing = sourceFile.getImportDeclaration(moduleSpecifier);
    if (!existing) {
      sourceFile.addImportDeclaration({ moduleSpecifier, namedImports: [namedImport] });
      modifiedLines++;
    }
  }

  if (payload.setVariable) {
    const { name, value } = payload.setVariable;
    const decl = sourceFile.getVariableDeclaration(name);
    if (decl) {
      decl.setInitializer(JSON.stringify(value));
      modifiedLines++;
    }
  }

  const newFrontmatter = sourceFile.getFullText();
  newSource = `---\n${newFrontmatter}\n---\n${templateBlock}`;
}

// ─── Mode B: Template Mutation (@astrojs/compiler + position surgery) ────────

else {
  let result;
  try {
    result = await parse(rawSource, { position: true });
  } catch (e) {
    die("PARSE_ERROR", `@astrojs/compiler failed to parse ${path.basename(filepath)}: ${e.message}`);
  }

  const ast = result.ast;

  // Walk the AST looking for element(s) matching targetSelector
  // @astrojs/compiler nodes carry a `position` field with start/end offsets
  let targetNode = null;
  const discovered = [];

  function walk(node) {
    if (!node) return;
    if (node.type === "element") {
      discovered.push(node.name);
      if (node.name === targetSelector) {
        targetNode = node;
        return; // stop at first match
      }
    }
    const children = node.children || node.body?.nodes || [];
    children.forEach(walk);
  }

  walk(ast);

  if (!targetNode) {
    out({
      status: "error",
      reason: "TARGET_NOT_FOUND",
      target: targetSelector,
      available_components: [...new Set(discovered)].slice(0, 20),
    });
    process.exit(1);
  }

  // Position-aware string surgery on the raw source
  // The node's position.start.offset gives us the character index of '<'
  // We find the end of the opening tag '>' to insert attributes before it
  const tagStart = targetNode.position?.start?.offset ?? -1;
  if (tagStart === -1) {
    die("NO_POSITION_DATA", "Parser did not return position offsets for target node.");
  }

  // Find the closing '>' or '/>' of the opening tag
  let tagEnd = tagStart;
  while (tagEnd < rawSource.length && rawSource[tagEnd] !== ">") tagEnd++;
  // If self-closing, step back before '/>'
  const isSelfClosing = rawSource[tagEnd - 1] === "/";
  const insertAt = isSelfClosing ? tagEnd - 1 : tagEnd;

  let injectionStr = "";

  if (payload.setAttributes) {
    for (const [k, v] of Object.entries(payload.setAttributes)) {
      injectionStr += ` ${k}="${v}"`;
      modifiedLines++;
    }
  }
  if (payload.addClass) {
    // Check if class attribute already exists in the raw tag region
    const tagRegion = rawSource.slice(tagStart, tagEnd);
    const classMatch = tagRegion.match(/class="([^"]*)"/);
    if (classMatch) {
      injectionStr = rawSource.slice(0, tagStart) +
        tagRegion.replace(/class="([^"]*)"/, `class="$1 ${payload.addClass}"`) +
        rawSource.slice(tagEnd);
      modifiedLines++;
      newSource = injectionStr;
      injectionStr = null; // signal we already built newSource
    } else {
      injectionStr += ` class="${payload.addClass}"`;
      modifiedLines++;
    }
  }

  if (injectionStr !== null) {
    newSource = rawSource.slice(0, insertAt) + injectionStr + rawSource.slice(insertAt);
  }
}


// ─── Write to Disk ────────────────────────────────────────────────────────────

fs.writeFileSync(filepath, newSource, "utf8");

out({
  status: "success",
  file: path.basename(filepath),
  modified_lines: modifiedLines,
});
