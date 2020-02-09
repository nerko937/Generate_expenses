window.addEventListener('DOMContentLoaded', (event) => {

  // Dropdown events
  dropdowns = document.querySelectorAll('.month-dropdown')
  if (dropdowns.length) {
    dropdowns.forEach(element => {
      const column = element.parentElement.parentElement.parentElement.parentElement
      const className = column.classList.contains('has-background-info')
        ? 'has-text-info' : 'has-text-primary'
      const span = element.querySelector('span')
      element.addEventListener('click', (event) => {
        element.classList.add('is-active')
      })
      element.addEventListener('mouseenter', (event) => {
        span.classList.add(className)
      })
      element.addEventListener('mouseleave', (event) => {
        element.classList.remove('is-active')
        span.classList.remove(className)
      })
    })
    
  }
})
