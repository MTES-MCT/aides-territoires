import { Controller } from '../../@hotwired/stimulus/dist/stimulus.js'

export default class extends Controller {
  departments = {}
  communes = {}
  communesData = {}
  zoomFrance = 5.5
  centerFrance = [46.227, 2.213]
  defaultFillStyle = {
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.6,
  }
  defaultHoverStyle = {
    weight: 4,
    dashArray: '',
    fillOpacity: 0.7,
  }
  static targets = [
    'regions',
    'regionsOrgCounts',
    'departments',
    'departmentsOrgCounts',
    'communes',
    'communesWithOrg',
    'epcisWithOrg',
    'tables',
  ]
  static values = {
    regionsOrgCommunesMax: Number,
    departmentsOrgCommunesMax: Number,
  }

  #_forwardRegularEvent(e) {
    // This is a hack because Leaflet does not dispatch regular events,
    // so we created that proxy to be able to bind them using Stimulus
    // from the HTML: `data-action="map:moveend->map#switchShapes"`.
    this.dispatch(e.type, { detail: e })
  }

  connect() {
    // Styles to retrieve colors from CSS variables (DesignSystem).
    this.styles = getComputedStyle(document.documentElement)
    this.defaultHoverStyle.color = this.styles.getPropertyValue(
      '--blue-france-sun-113-625'
    )
    // Counts/existence given the perimeter.
    this.regionsOrgCounts = JSON.parse(this.regionsOrgCountsTarget.textContent)
    this.departmentsOrgCounts = JSON.parse(this.departmentsOrgCountsTarget.textContent)
    this.communesWithOrg = JSON.parse(this.communesWithOrgTarget.textContent)
    this.epcisWithOrg = JSON.parse(this.epcisWithOrgTarget.textContent)
    // Compute density scales for map’s legend.
    this.scaleRegions = utils.generateScale(this.regionsOrgCommunesMaxValue, 7)
    this.scaleDepartments = utils.generateScale(this.departmentsOrgCommunesMaxValue, 7)
    // Only now can we create the map with correct data.
    this.map = this.#initMap()
    this.map.on('moveend', this.#_forwardRegularEvent, this)
  }

  switchShapes() {
    // These two values are empirical, on load, when you zoom in
    // then zoom out you should get back to the same shapes level.
    const zoomRegion = this.zoomFrance + 0.5
    const zoomDepartment = zoomRegion + 2.5
    const currentZoomLevel = this.map.getZoom()
    const regionLevel = currentZoomLevel <= zoomRegion
    const departmentLevel =
      currentZoomLevel > zoomRegion && currentZoomLevel < zoomDepartment
    const communeLevel = currentZoomLevel >= zoomDepartment
    if (regionLevel) {
      this.#switchToRegionLevel()
    } else if (departmentLevel) {
      this.#switchToDepartmentLevel()
    } else if (communeLevel) {
      this.#switchToCommuneLevel()
    }
  }

  #switchToRegionLevel() {
    this.map.hasLayer(this.departments) && this.map.removeLayer(this.departments)
    if (this.map.hasLayer(this.regions)) return
    this.map.addLayer(this.regions)
    this.legend.setContent(this.#generateLegendContent(this.scaleRegions))
    if (this.tableTarget) this.tableTarget.innerHTML = ''
  }

  #switchToDepartmentLevel() {
    this.map.hasLayer(this.regions) && this.map.removeLayer(this.regions)
    for (let commune of Object.values(this.communes)) {
      this.map.removeLayer(commune)
    }
    if (this.map.hasLayer(this.departments)) return
    if (this.departments.length) {
      this.map.addLayer(this.departments)
    } else {
      this.#getDepartments().then((departments) => {
        this.departments = departments
        this.map.addLayer(departments)
      })
    }
    this.legend.setContent(this.#generateLegendContent(this.scaleDepartments))
    if (this.tableTarget) this.tableTarget.innerHTML = ''
  }

  #switchToCommuneLevel() {
    this.map.hasLayer(this.regions) && this.map.removeLayer(this.regions)
    this.map.hasLayer(this.departments) && this.map.removeLayer(this.departments)

    // We determine the current department being the one at the center of the map.
    const insideLayers = mapUtils.pointInLayer(
      this.map.getCenter(),
      this.departments,
      true
    )
    if (!insideLayers.length) return
    const currentDepartmentCode = insideLayers[0].feature.properties.code

    if (this.communes[currentDepartmentCode]) {
      this.map.addLayer(this.communes[currentDepartmentCode])
      this.#updateTable(this.communesData[currentDepartmentCode])
    } else {
      this.#getCommunes(currentDepartmentCode).then(({ communes, data }) => {
        this.communes[currentDepartmentCode] = communes
        this.communesData[currentDepartmentCode] = data
        this.map.addLayer(communes)
        this.#updateTable(data)
      })
    }
    this.legend.setContent(`
      <i style="background:purple;"></i> Inscriptions multiples<br>
      <i style="background:${this.#getAgeColor(3)};"></i> Ces 30 derniers jours<br>
      <i style="background:${this.#getAgeColor(2)};"></i> Dans le dernier trimestre<br>
      <i style="background:${this.#getAgeColor(1)};"></i> Inscription plus ancienne<br>
      <i style="background:${this.#getAgeColor(4)};"></i> Inscription d’un EPCI
    `)
  }

  #updateTable(data) {
    const correspondanceCommunes = []
    const correspondanceEpcis = []
    for (const feature of data.features) {
      const key = `${feature.properties.code}-${feature.properties.nom}`
      if (Object.keys(this.communesWithOrg).includes(key)) {
        this.communesWithOrg[key].forEach((org) => {
          correspondanceCommunes.push({
            nom: feature.properties.nom,
            organization_name: org.organization_name,
            date_created: org.date_created,
            projects_count: org.projects_count,
            user_email: org.user_email,
          })
        })
      }
      if (Object.keys(this.epcisWithOrg).includes(key)) {
        this.epcisWithOrg[key].forEach((org) => {
          correspondanceEpcis.push({
            nom: feature.properties.nom,
            organization_name: org.organization_name,
            date_created: org.date_created,
            projects_count: org.projects_count,
            user_email: org.user_email,
          })
        })
      }
    }
    const department = data.features[0].properties.departement
    correspondanceCommunes.sort((a, b) => b.date_created > a.date_created)
    correspondanceEpcis.sort((a, b) => b.date_created > a.date_created)
    this.tablesTarget.innerHTML = `
      <h2>
        Communes et leurs organisations (département ${department})
      </h2>
      <div class="fr-alert fr-alert--info">
        <p>
          Ce tableau comporte l’ensemble des communes
          (incluant les doublons/inscriptions multiples pour un même périmètre).
        </p>
      </div>
      <table
        data-controller="table"
        data-downloadable="true"
        data-table-target="table"
        class="fr-table fr-table--layout-fixed fr-table--no-caption">
        <caption>Communes et leurs organisations (${department}) :</caption>
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
            <th
              scope="col"
              aria-sort="descending"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="date"
              >Date de création</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="number"
              >Nombre de projets</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Courriels</th>
          </tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            ${correspondanceCommunes
              .map(
                (item) =>
                  `
                  <td scope="row">${item.nom}</td>
                  <td>${item.organization_name}</td>
                  <td>${new Date(item.date_created).toLocaleDateString('fr-FR')}</td>
                  <td>${item.projects_count}</td>
                  <td>${item.user_email}</td>
                  `
              )
              .join('</tr><tr data-table-target="row">')}
          </tr>
        </tbody>
      </table>
      <h2>
        EPCI et leurs organisations (département ${department})
      </h2>
      <div class="fr-alert fr-alert--info">
        <p>
          Ce tableau comporte l’ensemble des EPCI
          (incluant les doublons/inscriptions multiples pour un même périmètre).
        </p>
      </div>
      <table
        data-controller="table"
        data-downloadable="true"
        data-table-target="table"
        class="fr-table fr-table--layout-fixed fr-table--no-caption">
        <caption>EPCI et leurs organisations (${department}) :</caption>
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
            <th
              scope="col"
              aria-sort="descending"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="date"
              >Date de création</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="number"
              >Nombre de projets</th>
            <th
              scope="col"
              data-action="click->table#sortTable"
              data-table-target="header"
              data-type="text"
              >Courriels</th>
          </tr>
        </thead>
        <tbody data-table-target="body">
          <tr data-table-target="row">
            ${correspondanceEpcis
              .map(
                (item) =>
                  `
                  <td scope="row">${item.nom}</td>
                  <td>${item.organization_name}</td>
                  <td>${new Date(item.date_created).toLocaleDateString('fr-FR')}</td>
                  <td>${item.projects_count}</td>
                  <td>${item.user_email}</td>
                  `
              )
              .join('</tr><tr data-table-target="row">')}
          </tr>
        </tbody>
      </table>
    `
  }

  #initMap() {
    const map = this.#createMap()
    // Control that shows state info on hover.
    this.info = this.#createInfo()
    map.addControl(this.info)
    // Control that shows the legend for colors.
    this.legend = this.#createLegend()
    map.addControl(this.legend)
    this.regions = this.#getRegions()
    // By default, we load regions’ shapes.
    this.regions.addTo(map)
    return map
  }

  #createMap() {
    const map = L.map(this.element.querySelector('div')).setView(
      this.centerFrance,
      this.zoomFrance
    )
    map.attributionControl.addAttribution(
      'Contours &copy; <a href="https://github.com/etalab/contours-administratifs">Etalab</a>'
    )
    L.tileLayer('https://{s}.forte.tiles.quaidorsay.fr/fr{r}/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: `&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
        et Quai d’Orsay`,
    }).addTo(map)
    return map
  }

  #createInfo() {
    L.HoverInfo = L.Control.extend({
      onAdd: function () {
        this._div = L.DomUtil.create('div', 'info')
        this.update(null, this.regionsOrgCounts)
        return this._div
      },
      update: function (props, counts) {
        let message = '<h4>Périmètre</h4>'
        if (!props) {
          message += 'Survoler une zone'
        } else {
          if (props.code in counts) {
            const communeCount = counts[props.code]['communes_count'] || 0
            const epciCount = counts[props.code]['epcis_count'] || 0
            message += `<strong>${props.nom}</strong><br>`
            if ('percentage_communes' in counts[props.code]) {
              message += `${communeCount} communes (soit ${
                counts[props.code]['percentage_communes'].toString().replace('.', ',')
              }&#8239;%) / ${epciCount} EPCI`
            } else {
              message += `${communeCount} communes / ${epciCount} EPCI`
            }
          } else {
            message += `
              ${counts['name']} (${counts['communes_count']} communes /
              ${counts['epcis_count']} EPCI)<br>
            `
            message += `<strong>${props.nom}</strong>`
            if (props.date_created) {
              message += ` (${props.date_created.toLocaleDateString('fr-FR')})`
            }
            if (props.extraInfo) {
              message += `<br>${props.extraInfo}`
            }
          }
        }
        this._div.innerHTML = message
      },
    })
    return new L.HoverInfo()
  }

  #createLegend() {
    L.Legend = L.Control.extend({
      onAdd: function () {
        const container = document.createElement('div')
        container.classList.add('info', 'legend')
        if (this.options.content) {
          container.innerHTML = this.options.content
        }
        return container
      },
      setContent: function (str) {
        this.getContainer().innerHTML = str
      },
    })

    return new L.Legend({
      position: 'bottomleft',
      content: this.#generateLegendContent(this.scaleRegions),
    })
  }

  #generateLegendContent(scale) {
    const labels = []
    let from, to

    for (let i = 0; i < scale.length; i++) {
      from = scale[i]
      to = scale[i + 1]

      const color = this.#getDensityColor(from + 1, scale)
      labels.push(
        `<i style="background:${color};"></i> ${from} ${to ? '&ndash;' + to : '+'}`
      )
    }
    return labels.join('<br>')
  }

  #getRegions() {
    const regionsShapes = JSON.parse(this.regionsTarget.textContent)
    const regions = L.geoJson([regionsShapes], {
      style: (feature) => {
        const fillColor = {
          fillColor: this.#getDensityColor(
            this.regionsOrgCounts[feature.properties.code]['communes_count'] || 0,
            this.scaleRegions
          ),
        }
        return { ...this.defaultFillStyle, ...fillColor }
      },
      onEachFeature: (_feature, layer) => {
        layer.on({
          mouseover: (e) => {
            const target = e.target
            target.setStyle(this.defaultHoverStyle)

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              target.bringToFront()
            }

            this.info.update(target.feature.properties, this.regionsOrgCounts)
          },
          mouseout: (e) => {
            regions.resetStyle(e.target)
            this.info.update(null, this.regionsOrgCounts)
          },
          click: this.#fitMap.bind(this),
        })
      },
    })
    return regions
  }

  #getDepartments() {
    return fetch(this.departmentsTarget.dataset.src)
      .then(this.#checkResponse)
      .then((data) => {
        const departments = L.geoJson(data, {
          style: (feature) => {
            const fillColor = {
              fillColor: this.#getDensityColor(
                this.departmentsOrgCounts[feature.properties.code]['percentage_communes'] ||
                  0,
                this.scaleDepartments
              ),
            }
            return { ...this.defaultFillStyle, ...fillColor }
          },
          onEachFeature: (_feature, layer) => {
            layer.on({
              mouseover: (e) => {
                const target = e.target
                target.setStyle(this.defaultHoverStyle)

                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                  target.bringToFront()
                }

                this.info.update(target.feature.properties, this.departmentsOrgCounts)
              },
              mouseout: (e) => {
                departments.resetStyle(e.target)
                this.info.update(null, this.departmentsOrgCounts)
              },
              click: this.#fitMap.bind(this),
            })
          },
        })
        return departments
      })
      .catch((ex) => {
        console.log('No available shapes for departments?', ex)
      })
  }

  #getCommunes(code) {
    return fetch(this.communesTarget.getAttribute(`data-src-${code}`))
      .then(this.#checkResponse)
      .then((data) => {
        const communes = L.geoJson(data, {
          style: (feature) => {
            const key = `${feature.properties.code}-${feature.properties.nom}`
            let additionalStyles = {}
            if (Object.keys(this.communesWithOrg).includes(key)) {
              const communes = this.communesWithOrg[key]
              if (communes.length == 1) {
                additionalStyles.fillColor = this.#getAgeColor(communes[0].age)
              } else {
                // Make visible communes with more than one entry!
                additionalStyles.fillColor = 'purple'
              }
            }
            if (Object.keys(this.epcisWithOrg).includes(key)) {
              additionalStyles.dashArray = ''
              additionalStyles.weight = 2
              additionalStyles.color = this.styles.getPropertyValue('--info-425-625')
            }
            return { ...this.defaultFillStyle, ...additionalStyles }
          },
          onEachFeature: (_feature, layer) => {
            layer.on({
              mouseover: (e) => {
                const target = e.target
                target.setStyle(this.defaultHoverStyle)

                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                  target.bringToFront()
                }

                const properties = target.feature.properties
                const counts = this.departmentsOrgCounts[properties.departement]
                const key = `${properties.code}-${properties.nom}`
                const epciHasOrg = Object.keys(this.epcisWithOrg).includes(key)
                const communeHasOrg = Object.keys(this.communesWithOrg).includes(key)
                properties.extraInfo = ''
                if (communeHasOrg) {
                  const communes = this.communesWithOrg[key]
                  const communeProperties = communes[0]
                  properties.date_created = new Date(communeProperties['date_created'])
                  if (communes.length > 1) {
                    properties.extraInfo += communes
                      .map((commune) => {
                        return `<span aria-hidden="true">⚠️</span> ${commune['organization_name']}`
                      })
                      .join('<br>')
                    properties.extraInfo += '<br>'
                  }
                }
                if (epciHasOrg) {
                  properties.extraInfo += this.epcisWithOrg[key]
                    .map((epci) => {
                      return `${epci['organization_name']} (${new Date(
                        epci['date_created']
                      ).toLocaleDateString('fr-FR')})`
                    })
                    .join('<br>')
                }
                this.info.update(properties, counts)
              },
              mouseout: (e) => {
                communes.resetStyle(e.target)
                this.info.update(null, {})
              },
              click: this.#fitMap.bind(this),
            })
          },
        })
        return { communes, data }
      })
      .catch((ex) => {
        console.log(
          `No available communes shapes for that department code ${code}?`,
          ex
        )
      })
  }

  #checkResponse(response) {
    if (response.ok) {
      return response.json()
    }
    throw response.statusText
  }

  #fitMap(e) {
    this.map.fitBounds(e.target.getBounds())
  }

  // Get color depending on density value
  #getDensityColor(density, scale) {
    // Gradient of CSS colors from France DesignSystem from lighter to darker.
    const gradientBlue = [
      '--blue-france-975-75',
      '--blue-france-950-100',
      '--blue-france-925-125',
      '--blue-france-850-200',
      '--blue-france-main-525',
      '--blue-france-sun-113-625-hover',
      '--blue-france-sun-113-625',
      '--grey-50-1000',
    ]
    // Creates an object to access the color name from a scale number.
    const scaleToColor = [utils.zip([scale, gradientBlue])].map(Object.fromEntries)[0]
    const color = scaleToColor[utils.closestInArray(density, scale)]
    return this.styles.getPropertyValue(color)
  }

  #getAgeColor(age) {
    const gradientRed = [
      '--yellow-tournesol-950-100-hover', // Jaune.
      '--warning-425-625-hover', // Orange.
      '--red-marianne-main-472', // Rouge.
      '--info-425-625', // Bleu.
    ]
    const color = gradientRed[age - 1]
    return this.styles.getPropertyValue(color)
  }

  flyTo(e) {
    e.preventDefault()
    // Necessary to be able to display communes.
    this.#switchToDepartmentLevel()
    this.map.flyTo(JSON.parse(e.target.dataset.latlon), Number(e.target.dataset.zoom))
  }
}

const utils = (function () {
  // Something utils to move to their dedicated file?

  function generateScale(max, nbItems) {
    // generateScale(477, 7) => [0, 69, 137, 205, 273, 341, 409, 477]
    // See https://stackoverflow.com/a/47968178
    // and https://poopcode.com/divide-a-number-into-x-parts-in-javascript/
    return [0].concat(
      [...Array(nbItems)]
        .map((_, index) => 0 | (max / nbItems + (index < max % nbItems)))
        .map(((acc) => (val) => (acc += val))(0))
    )
  }
  function zip(rows) {
    // Equivalent to zip() in Python.
    // zip([['foo', 'bar'], [1, 2]]) => [['foo', 1], ['bar', 2]]
    // See https://stackoverflow.com/a/10284006
    return rows[0].map((_, index) => rows.map((row) => row[index]))
  }
  function closestInArray(needle, haystack) {
    // closestInArray(10, [1, 4, 9, 12]) => 9
    // See https://stackoverflow.com/a/35000557
    return haystack.reduce((prev, curr) =>
      Math.abs(curr - needle) < Math.abs(prev - needle) ? curr : prev
    )
  }
  return { generateScale, zip, closestInArray }
})()

const mapUtils = (function () {
  // Something map-related utils to move to their dedicated file?

  function boundingBoxAroundPolyCoords(coords) {
    // From https://github.com/maxogden/geojson-js-utils
    let xAll = []
    let yAll = []

    for (let coord of coords[0]) {
      xAll.push(coord[1])
      yAll.push(coord[0])
    }

    xAll = xAll.sort((a, b) => a - b)
    yAll = yAll.sort((a, b) => a - b)

    return [
      [xAll[0], yAll[0]],
      [xAll[xAll.length - 1], yAll[yAll.length - 1]],
    ]
  }

  function pointInBoundingBox(point, bounds) {
    // From https://github.com/maxogden/geojson-js-utils
    return !(
      point.coordinates[1] < bounds[0][0] ||
      point.coordinates[1] > bounds[1][0] ||
      point.coordinates[0] < bounds[0][1] ||
      point.coordinates[0] > bounds[1][1]
    )
  }

  // Point in Polygon
  // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

  function pnpoly(x, y, coords) {
    // From https://github.com/maxogden/geojson-js-utils
    let vert = [[0, 0]]

    for (let coord of coords) {
      for (let subcoord of coord) {
        vert.push(subcoord)
      }
      vert.push(coord[0])
      vert.push([0, 0])
    }

    let inside = false
    for (let i = 0, j = vert.length - 1; i < vert.length; j = i++) {
      if (
        vert[i][0] > y != vert[j][0] > y &&
        x <
          ((vert[j][1] - vert[i][1]) * (y - vert[i][0])) / (vert[j][0] - vert[i][0]) +
            vert[i][1]
      )
        inside = !inside
    }

    return inside
  }

  function pointInPolygon(p, poly) {
    // From https://github.com/maxogden/geojson-js-utils
    const coords = poly.type == 'Polygon' ? [poly.coordinates] : poly.coordinates

    let insideBox = false
    for (let coord of coords) {
      if (pointInBoundingBox(p, boundingBoxAroundPolyCoords(coord))) insideBox = true
    }
    if (!insideBox) return false

    let insidePoly = false
    for (let coord of coords) {
      if (pnpoly(p.coordinates[1], p.coordinates[0], coord)) insidePoly = true
    }

    return insidePoly
  }

  function isPoly(l) {
    // From https://github.com/mapbox/leaflet-pip/
    return (
      l.feature &&
      l.feature.geometry &&
      l.feature.geometry.type &&
      ['Polygon', 'MultiPolygon'].indexOf(l.feature.geometry.type) !== -1
    )
  }

  function pointInLayer(p, layer, first) {
    // From https://github.com/mapbox/leaflet-pip/
    p = [p.lng, p.lat]

    const results = []

    layer.eachLayer(function (l) {
      if (first && results.length) return

      if (
        isPoly(l) &&
        pointInPolygon({ type: 'Point', coordinates: p }, l.toGeoJSON().geometry)
      ) {
        results.push(l)
      }
    })
    return results
  }

  return { pointInLayer }
})()
