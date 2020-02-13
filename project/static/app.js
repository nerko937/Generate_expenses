window.addEventListener('DOMContentLoaded', (event) => {

  // Dropdown events
  dropdowns = document.querySelectorAll('.month-dropdown')
  if (dropdowns.length) {
    dropdowns.forEach(element => {
      const column = element.parentElement.parentElement.parentElement.parentElement
      const className = column.classList.contains('has-background-info')
        ? 'has-text-info' : 'has-text-primary'
      const span = element.querySelector('span')
      element.addEventListener('mouseenter', (event) => {
        element.classList.toggle('is-active')
        span.classList.toggle(className)
      })
      element.addEventListener('mouseleave', (event) => {
        element.classList.toggle('is-active')
        span.classList.toggle(className)
      })
      const dropdownMenu = element.querySelector('.dropdown-menu')
      dropdownMenu.addEventListener('mouseenter', (event) => {
        span.classList.toggle(className)
      })
      dropdownMenu.addEventListener('mouseleave', (event) => {
        span.classList.toggle(className)
      })
    })
  }
    
  // Notification close button event
  closeBtns = document.querySelectorAll('.notification .delete')
  if (closeBtns.length) {
    closeBtns.forEach((element) => {
      element.addEventListener('click', (event) => {
        element.parentElement.remove()
      })
    })
  }

})
