#!/usr/bin/env node

import { lstat, mkdir, mkdtemp, readFile, rename, rm, rmdir, stat, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { parseArgs } from 'node:util';
import { getSupportedAgents, installSkills } from 'skills';

const skillName = 'hermes-agent-docs-skill';
const repository = 'tbdavid2019/hermes-agent-docs-skill';
const marker = '.hermes-agent-docs-skill-npm';
const sha = /^[a-f0-9]{40}$/;

async function existingRevision(target) {
  let entry;
  try {
    entry = await lstat(target);
  } catch (error) {
    if (error.code === 'ENOENT') return undefined;
    throw error;
  }

  if (entry.isDirectory()) {
    try {
      await lstat(join(target, '.git'));
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
      const revision = await readFile(join(target, marker), 'utf8').catch((error) => {
        if (error.code === 'ENOENT') return '';
        throw error;
      });
      if (sha.test(revision.trim())) return revision.trim();
    }
  }
  throw new Error(`Installation already exists at ${target}. Update it with its original installer or choose another scope.`);
}

async function validateSnapshot(directory, commit) {
  const requiredFiles = ['SKILL.md', 'references/catalog.md', 'references/index.md'];
  for (const name of requiredFiles) {
    const file = await stat(join(directory, name));
    if (!file.isFile() || file.size === 0) throw new Error(`Invalid snapshot file: ${name}`);
  }
  const source = await readFile(join(directory, 'references/SOURCE.md'), 'utf8');
  const upstreamCommit = source.match(/^- Source commit: `([a-f0-9]{40})`$/m)?.[1];
  const syncedAt = source.match(/^- Synced at: `(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)`$/m)?.[1];
  if (typeof commit !== 'string' || !sha.test(commit)) throw new Error('Missing skill repository commit');
  if (typeof upstreamCommit !== 'string' || !sha.test(upstreamCommit)) {
    throw new Error('Invalid upstream documentation commit');
  }
  if (!syncedAt || Number.isNaN(Date.parse(syncedAt))) {
    throw new Error('Invalid documentation sync time');
  }
  return { upstreamCommit, syncedAt };
}

async function install(target) {
  const previousRevision = await existingRevision(target);
  const parent = dirname(target);
  await mkdir(parent, { recursive: true });
  const staging = await mkdtemp(join(parent, '.hermes-agent-docs-skill-'));
  let keepBackup = false;
  try {
    console.log('Fetching the latest Hermes Agent documentation snapshot…');
    const result = await installSkills(repository, {
      cwd: staging,
      ref: 'main',
      skills: [skillName],
      agents: ['universal'],
      mode: 'copy',
      lockfile: false,
      symlinks: 'reject',
      telemetry: false,
    });
    const [installed] = result.installed;
    if (result.failed.length || !installed) {
      throw new Error(result.failed.map(({ message }) => message).join('\n') || 'No skill was installed');
    }
    const commit = result.source.commit;
    const { upstreamCommit, syncedAt } = await validateSnapshot(installed.path, commit);
    await writeFile(join(installed.path, marker), `${commit}\n`, { flag: 'wx' });

    const lock = join(parent, '.hermes-agent-docs-skill-install.lock');
    try {
      await mkdir(lock);
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      throw new Error(`Another installation is using ${target}. Try again after it finishes.`);
    }
    try {
      if (await existingRevision(target) !== previousRevision) {
        throw new Error(`Installation changed while fetching the snapshot. Run the command again to update ${target}.`);
      }
      const backup = join(staging, 'previous-installation');
      if (previousRevision) await rename(target, backup);
      try {
        await rename(installed.path, target);
      } catch (error) {
        if (previousRevision) {
          try {
            await rename(backup, target);
          } catch (restoreError) {
            keepBackup = true;
            throw new AggregateError([error, restoreError], `Previous installation is available at ${backup}`);
          }
        }
        throw error;
      }
    } finally {
      await rmdir(lock);
    }

    console.log(`Installation directory: ${target}`);
    console.log(`Skill repository commit: ${commit}`);
    console.log(`Upstream documentation commit: ${upstreamCommit}`);
    console.log(`Documentation synced at: ${syncedAt}`);
  } finally {
    if (!keepBackup) await rm(staging, { recursive: true, force: true });
  }
}

async function main() {
  const { values } = parseArgs({
    options: {
      agent: { type: 'string', short: 'a', default: 'codex' },
      global: { type: 'boolean', short: 'g' },
      help: { type: 'boolean', short: 'h' },
    },
  });
  if (values.help) {
    console.log(`Usage: npx -y hermes-agent-docs-skill@latest [--agent <id>] [--global]

Install or refresh the latest documentation snapshot from GitHub.
  -a, --agent <id>   Target agent (default: codex)
  -g, --global       Install in the agent's user directory
  -h, --help         Show this help`);
    return;
  }

  const agent = getSupportedAgents().find(({ id }) => id === values.agent);
  if (!agent) throw new Error(`Unknown agent: ${values.agent}`);
  const skillsDirectory = values.global ? agent.globalSkillsDir : agent.projectSkillsDir;
  if (!skillsDirectory) throw new Error(`${agent.name} only supports project installation`);
  await install(resolve(skillsDirectory, skillName));
}

main().catch((error) => {
  console.error(`hermes-agent-docs-skill: ${error.message}`);
  process.exitCode = 1;
});


