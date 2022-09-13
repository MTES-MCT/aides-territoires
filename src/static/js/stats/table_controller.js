import { Controller } from 'https://unpkg.com/@hotwired/stimulus/dist/stimulus.js'

export default class extends Controller {
  static targets = ['header', 'body', 'row']

  connect() {
    this.headerTargets.forEach((header) => {
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
      header.querySelector('.table-arrows').innerText = sort === 'ascending' ? '↓' : '↑'
    }
  }

  sortTable(event) {
    const header = event.target.closest('th')
    const current = header.getAttribute('aria-sort')
    const sort = current === 'ascending' ? 'descending' : 'ascending'
    // Reset all headers,
    this.headerTargets.forEach((header) => {
      header.removeAttribute('aria-sort')
      header.querySelector('.table-arrows').innerText = '↑↓'
    })
    // then set for the current header.
    header.setAttribute('aria-sort', sort)
    header.querySelector('.table-arrows').innerText = sort === 'ascending' ? '↓' : '↑'

    let values = []
    const columnIndex = this.#siblingIndex(header)
    const tdSelector = 'td:nth-child(' + (columnIndex + 1) + ')'
    this.rowTargets.forEach((row) => {
      const node = row.querySelector(tdSelector)
      let val = node.innerText
      if (!isNaN(val)) {
        val = parseFloat(val)
      }
      values.push({ value: val, row: row })
    })

    const dataType = header.dataset.type
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
    const textA = (a.value + '').toUpperCase()
    const textB = (b.value + '').toUpperCase()
    if (textA < textB) return -1
    if (textA > textB) return 1
    return 0
  }
}
