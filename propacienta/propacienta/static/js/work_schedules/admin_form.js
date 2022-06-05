
const timeFieldEl = document.getElementById('id_time_field').parentNode.parentNode.parentNode
var c = 1
const defaultValueBreakField = '00:00-00:00'
function parseBreaks() {
    let elem = document.getElementById('id_breaks');
    let breaks = JSON.parse(elem.value)
    // console.log(breaks, typeof breaks)
    return breaks
}
let getNodes = str => new DOMParser().parseFromString(str, 'text/html').body.firstChild;
function renderAddBreakBtn() {
    let elBreakField = document.getElementById('id_time_field').parentNode
    const addBreakBtn = '<a onclick="addBreakHandle(event)" class="related-widget-wrapper-link add-related" id="add_break" href="#" title="Добавить ещё один Перерыв"><img src="/static/admin/img/icon-addlink.svg" alt="Добавить"></a>'
    elBreakField.appendChild(getNodes(addBreakBtn))
}
function addBreakField(hourstart, minutestart, hourend, minuteend) {
    const deleteBreakBtn = '<a onclick="deleteBreakHandle(event)" class="related-widget-wrapper-link add-related del-break-btn" href="#" title="Удалить Перерыв"><img src="/static/admin/img/icon-deletelink.svg" alt="Удалить"></a>'
    const elstart = '<div class="form-row field-time_field"><div><label class="required" for="id_time_field">Перерыв:</label><input type="text" name="time_field" value="'
    const elend = `" required="" id="id_time_field">${deleteBreakBtn}</div></div>`
    timeFieldEl.append(getNodes(elstart + `${hourstart}:${minutestart}-${hourend}:${minuteend}` + elend))
}
function renderBreaksFields() {
    // var c = 1
    let breaks = parseBreaks()
    if (breaks.breaks != undefined) {
        breaks.breaks.forEach(element => {
            let hourstart = element.start.slice(0, 2)
            let minutestart = element.start.slice(2)
            let hourend = element.end.slice(0, 2)
            let minuteend = element.end.slice(2)
            addBreakField(hourstart, minutestart, hourend, minuteend)
        });
    }
}
function addBreak(breakStart, breakEnd) {
    let breaks = parseBreaks()
    let elem = document.getElementById('id_breaks');
    if (breaks.breaks != undefined) {
        breaks.breaks.push({ 'start': breakStart, 'end': breakEnd })
        elem.value = JSON.stringify(breaks)
    } else {
        elem.value = JSON.stringify({ 'breaks': [{ 'start': breakStart, 'end': breakEnd }] })
    }
}
function deleteBreak(breakStart, breakEnd) {
    let breaks = parseBreaks()
    let elem = document.getElementById('id_breaks');
    if (breaks.breaks != undefined) {
        breaks.breaks = breaks.breaks.filter(elem => {
            return elem.start != breakStart && elem.end != breakEnd
        })
        elem.value = JSON.stringify(breaks)
    }
}
function validateBreak(hourstart, minutestart, hourend, minuteend) {
    if (parseInt(hourstart) < 0 || parseInt(hourstart) > 23) {
        return false
    }
    if (parseInt(minutestart) < 0 || parseInt(minutestart) > 59) {
        return false
    }
    if (parseInt(hourend) < 0 || parseInt(hourend) > 23) {
        return false
    }
    if (parseInt(minuteend) < 0 || parseInt(minuteend) > 59) {
        return false
    }
    let start = new Date()
    start.setHours(hourstart, minutestart)
    if (isNaN(start)) {
        return false
    }
    let end = new Date()
    end.setHours(hourend, minuteend)
    if (isNaN(end)) {
        return false
    }
    return start < end
}
function addBreakHandle(event) {
    event.preventDefault()
    event.stopPropagation()
    let elBreakField = document.getElementById('id_time_field')
    elBreakField.parentNode.parentNode.classList.remove("errors")
    const value = elBreakField.value
    if (value != defaultValueBreakField) {
        if (!validateBreak(value.slice(0, 2), value.slice(3, 5), value.slice(6, 8), value.slice(9, 11))) {
            elBreakField.parentNode.parentNode.classList.add("errors")
            return
        }
        addBreakField(value.slice(0, 2), value.slice(3, 5), value.slice(6, 8), value.slice(9, 11))
        elBreakField.value = defaultValueBreakField
        addBreak(value.slice(0, 2) + value.slice(3, 5), value.slice(6, 8) + value.slice(9, 11))
    }
}
function deleteBreakHandle(event) {
    event.preventDefault()
    event.stopPropagation()
    const elValue = event.currentTarget.previousSibling.value
    deleteBreak(elValue.slice(0, 2) + elValue.slice(3, 5), elValue.slice(6, 8) + elValue.slice(9, 11))
    event.currentTarget.parentNode.parentNode.remove()
}
// document.getElementById('id_breaks').disabled = true
renderAddBreakBtn()
renderBreaksFields()