import { Controller } from '../../@hotwired/stimulus/dist/stimulus.js'

export default class extends Controller {
  static targets = ['table', 'header', 'body', 'row']

  connect() {
    if (this.element.dataset.downloadable) this.#attachDownloadAsCSVLink()
    this.headerTargets.forEach((header) => {
      // Keep the original title for CSV export.
      header.dataset.val = header.textContent
      header.innerHTML = `
        <button
          type="button"
          title="${header.textContent} - Activer pour trier les colonnes"
          >
          <span class="table-arrows">↑↓</span>
          ${header.textContent}
        </button>
      `
    })
    const sorted = this.headerTargets.filter((header) =>
      header.hasAttribute('aria-sort')
    )
    if (sorted.length) {
      const header = sorted[0]
      const sort = header.getAttribute('aria-sort')
      header.querySelector('.table-arrows').textContent =
        sort === 'ascending' ? '↓' : '↑'
    }
  }

  sortTable(event) {
    const header = event.target.closest('th')
    const current = header.getAttribute('aria-sort')
    const sort = current === 'ascending' ? 'descending' : 'ascending'
    // Reset all headers,
    this.headerTargets.forEach((header) => {
      header.removeAttribute('aria-sort')
      header.querySelector('.table-arrows').textContent = '↑↓'
    })
    // then set for the current header.
    header.setAttribute('aria-sort', sort)
    header.querySelector('.table-arrows').textContent = sort === 'ascending' ? '↓' : '↑'

    let values = []
    const columnIndex = this.#siblingIndex(header)
    const tdSelector = 'td:nth-child(' + (columnIndex + 1) + ')'
    const dataType = header.dataset.type
    this.rowTargets.forEach((row) => {
      const node = row.querySelector(tdSelector)
      let val = node.dataset.value || node.textContent
      if (dataType === 'number' && val.includes(',')) {
        val = val.replace(',', '.')
      }
      if (!isNaN(val)) {
        val = parseFloat(val)
      }
      values.push({ value: val, row: row })
    })

    const sortFunction = this.#getSortFunction(dataType)
    values.sort(sortFunction.bind(this))
    if (sort === 'descending') values = values.reverse()
    // `.appendChild()` will sort in place if appending current elements.
    values.forEach((value) => this.bodyTarget.appendChild(value.row))
  }

  #getSortFunction(dataType) {
    if (dataType === 'text') {
      return this.#sortTextVal
    } else if (dataType === 'date') {
      return this.#sortDateVal
    } else if (dataType === 'number') {
      return this.#sortNumberVal
    }
  }

  #siblingIndex(node) {
    let count = 0

    while ((node = node.previousElementSibling)) {
      count++
    }

    return count
  }

  #sortNumberVal(a, b) {
    return a.value - b.value
  }

  #parseDate(value) {
    const parts = value.split('/')
    const isoDate = [parts[2], parts[1], parts[0]].join('-')
    return Date.parse(isoDate)
  }

  #sortDateVal(a, b) {
    return this.#parseDate(a.value) - this.#parseDate(b.value)
  }

  #sortTextVal(a, b) {
    return a.value.localeCompare(b.value, 'fr')
  }

  #attachDownloadAsCSVLink() {
    const footer = document.createElement('tfoot')
    const tr = document.createElement('tr')
    const td = document.createElement('td')
    td.setAttribute('colspan', this.headerTargets.length)
    td.style = 'text-align: center;'
    const downloadLink = document.createElement('a')
    downloadLink.classList.add('fr-btn', 'fr-fi-download-line', 'fr-btn--icon-left')
    downloadLink.href = '#'
    downloadLink.textContent = 'Télécharger en CSV'
    downloadLink.dataset.action = `${this.identifier}#downloadAsCSV`
    td.appendChild(downloadLink)
    tr.appendChild(td)
    footer.appendChild(tr)
    this.tableTarget.insertAdjacentElement('beforeend', footer)
  }

  downloadAsCSV(event) {
    event.preventDefault()
    const content = this.#getCSVContent()
    const name = this.element
      .querySelector('caption')
      .textContent.replace(/[:()]/gm, '')
      .trim()
      .replace(/(\s)/gm, '_')
    const filename = `export_${new Date().toLocaleDateString()}_${name}.csv`
    const csvFile = new Blob([content], { type: 'text/csv' })
    const fakeDownloadLink = document.createElement('a')
    fakeDownloadLink.download = filename
    fakeDownloadLink.dataset.csv = content
    fakeDownloadLink.href = window.URL.createObjectURL(csvFile)
    fakeDownloadLink.style.display = 'none'
    this.element.appendChild(fakeDownloadLink)
    fakeDownloadLink.click()
  }

  #getCSVContent() {
    const separator = ';'
    let csvRows = []
    // Only get direct children of the table in question (thead, tbody).
    Array.from(this.tableTarget.children).forEach((node) => {
      // Avoid adding the footer as we put the download link in it.
      if (node.tagName === 'TFOOT') return
      // Using scope to only get direct tr of node.
      node.querySelectorAll(':scope > tr').forEach((tr) => {
        let csvLine = []
        // Again scope to only get direct children.
        tr.querySelectorAll(':scope > th, :scope > td').forEach((td) => {
          // Clone as to not remove anything from original.
          let copytd = td.cloneNode(true)
          let data
          if (copytd.dataset.val) data = copytd.dataset.val
          else {
            data = copytd.textContent
          }
          data = data
            .replace(/(\r\n|\n|\r)/gm, '')
            .replace(/(\s\s)/gm, ' ')
            .trim()
            .replace(/"/g, '""')
          csvLine.push('"' + data + '"')
        })
        csvRows.push(csvLine.join(separator))
      })
    })
    return csvRows.join('\n')
  }
}
