import { Application } from '@hotwired/stimulus'
import { copyFileSync } from 'node:fs'

import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const replace = require('replace-in-file')

async function stimulusReady() {
  return new Promise((resolve) => {
    if (document.readyState == 'loading') {
      document.addEventListener('DOMContentLoaded', () => resolve())
    } else {
      resolve()
    }
  })
}

export function setupGlobalDom(dom) {
  require('jsdom-global')(dom)
  global.MutationObserver = window.MutationObserver
}

export async function setupStimulus(identifier, controller) {
  window.Stimulus = Application.start()
  window.Stimulus.register(identifier, controller)
  // window.Stimulus.debug = true
  await stimulusReady()
}

export async function importController(controllerPath) {
  const parts = controllerPath.split('/')
  const controllerPathname = parts[parts.length - 1]
  const target = `./tests/tmp/${controllerPathname}`
  copyFileSync(controllerPath, target)
  replace.sync({
    files: target,
    from: '../../@hotwired/stimulus/dist/stimulus.js',
    to: '@hotwired/stimulus',
  })
  const imported = await import(`./tmp/${controllerPathname}`)
  return imported.default
}
