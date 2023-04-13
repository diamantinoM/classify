function limitSize(select) {
    const renderedSelect = select.nextElementSibling.querySelector('ul');
    renderedSelect.style.height = '10rem';
    renderedSelect.style.overflowY = 'auto';
}

function main() {
    const selectElements = document.querySelectorAll('select.limit');
    selectElements.forEach(limitSize);
}

window.addEventListener('load', main);