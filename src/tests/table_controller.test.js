import { assert } from 'chai'
import { importController, setupGlobalDom, setupStimulus } from './stimulus_helpers.js'

const TableController = await importController('./static/js/stats/table_controller.js')

describe('Table', function () {
  it('Inject a button to sort columns (A11Y)', async function () {
    setupGlobalDom(`
      <table data-controller="table">
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Commune</th>
          <tr>
        </thead>
      </table>`)
    await setupStimulus('table', TableController)

    const th = document.querySelector('th')

    assert.strictEqual(
      th.innerHTML,
      `
        <button type="button" title="Commune - Activer pour trier les colonnes">
          <span class="table-arrows">↑↓</span>
          Commune
        </button>
      `
    )
    // Ensure we keep the original value of the cell too.
    assert.strictEqual(th.dataset.val, 'Commune')
  })

  it('Sort textual columns', async function () {
    setupGlobalDom(`
      <table data-controller="table">
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Commune</th>
          <tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            <td scope="row">Marseille</td>
          </tr>
          <tr data-table-target="row">
            <td scope="row">Arles</td>
          </tr>
        </tbody>
      </table>`)
    await setupStimulus('table', TableController)

    const th = document.querySelector('th')
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Marseille Arles'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑↓'
    )
    assert.strictEqual(document.querySelector('th').getAttribute('aria-sort'), null)

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Arles Marseille'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↓'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'ascending'
    )

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Marseille Arles'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'descending'
    )
  })

  it('Sort textual columns with aria-sort initially set', async function () {
    setupGlobalDom(`
      <table data-controller="table">
        <thead>
          <tr>
            <th
              scope="col"
              aria-sort="descending"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Commune</th>
          <tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            <td scope="row">Marseille</td>
          </tr>
          <tr data-table-target="row">
            <td scope="row">Arles</td>
          </tr>
        </tbody>
      </table>`)
    await setupStimulus('table', TableController)

    const th = document.querySelector('th')
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Marseille Arles'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'descending'
    )

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Arles Marseille'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↓'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'ascending'
    )

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      'Marseille Arles'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'descending'
    )
  })

  it('Sort numerical columns', async function () {
    setupGlobalDom(`
      <table data-controller="table">
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="number"
              >Inscriptions</th>
          <tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            <td scope="row">5</td>
          </tr>
          <tr data-table-target="row">
            <td scope="row">1</td>
          </tr>
        </tbody>
      </table>`)
    await setupStimulus('table', TableController)

    const th = document.querySelector('th')
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '5 1'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑↓'
    )
    assert.strictEqual(document.querySelector('th').getAttribute('aria-sort'), null)

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '1 5'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↓'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'ascending'
    )

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '5 1'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'descending'
    )
  })

  it('Sort date columns', async function () {
    setupGlobalDom(`
      <table data-controller="table">
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="date"
              >Date d’inscriptions</th>
          <tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            <td scope="row">05/08/2022</td>
          </tr>
          <tr data-table-target="row">
            <td scope="row">23/04/2022</td>
          </tr>
        </tbody>
      </table>`)
    await setupStimulus('table', TableController)

    const th = document.querySelector('th')
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '05/08/2022 23/04/2022'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑↓'
    )
    assert.strictEqual(document.querySelector('th').getAttribute('aria-sort'), null)

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '23/04/2022 05/08/2022'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↓'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'ascending'
    )

    th.click()
    assert.strictEqual(
      document.querySelector('tbody').textContent.replace(/\s+/g, ' ').trim(),
      '05/08/2022 23/04/2022'
    )
    assert.strictEqual(
      document.querySelector('th').querySelector('.table-arrows').textContent,
      '↑'
    )
    assert.strictEqual(
      document.querySelector('th').getAttribute('aria-sort'),
      'descending'
    )
  })

  it('Export table as CSV', async function () {
    setupGlobalDom(`
      <table data-controller="table"
        data-downloadable="true">
        <caption>Communes et leurs organisations (13) :</caption>
        <thead>
          <tr>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Commune</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Organisation</th>
          <tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            <td scope="row">Marseille</td>
            <td>Football</td>
          </tr>
          <tr data-table-target="row">
            <td scope="row">Arles</td>
            <td>Photographie</td>
          </tr>
        </tbody>
      </table>`)
    // See https://github.com/jsdom/jsdom/issues/1721#issuecomment-387279017
    if (typeof window.URL.createObjectURL === 'undefined') {
      Object.defineProperty(window.URL, 'createObjectURL', {
        value: (val) => 'csv-content',
      })
    }
    await setupStimulus('table', TableController)

    const tfoot = document.querySelector('tfoot')
    assert.strictEqual(tfoot.textContent.trim(), 'Télécharger en CSV')
    tfoot.querySelector('a').click()
    assert.include(
      document.querySelectorAll('table a')[1].getAttribute('download'),
      'Communes_et_leurs_organisations_13.csv'
    )
    assert.strictEqual(
      document.querySelectorAll('table a')[1].getAttribute('data-csv'),
      `"Commune";"Organisation"

"Marseille";"Football"
"Arles";"Photographie"`
    )
    // This is a trade-off given that we mock the whole `createObjectURL` function.
    assert.strictEqual(
      document.querySelectorAll('table a')[1].getAttribute('href'),
      'csv-content'
    )
  })
})
