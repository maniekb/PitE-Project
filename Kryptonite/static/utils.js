function createListItem(id, label, onclickStr) {
    return $('<li/>', {
        class: "dropdown-item currency-item",
        value: id,
        html: '<a href="#">' + label + '</a>',
        onclick: onclickStr
    })
}

function createDeletableButton(id, label, onclickStr) {
    return $('<button/>', {
        type: "button",
        class: "btn delete-button",
        value: id,
        html: label,
        onclick: onclickStr
    })
}