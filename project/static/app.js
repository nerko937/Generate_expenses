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

  // Redirect to month page with expenses
  monthUrls = document.querySelectorAll('.col-hover')
  if (monthUrls.length) {
    monthUrls.forEach((element) => {
      element.addEventListener('click', (event) => {
        window.location.href = element.dataset.href
      })
    })
  }

  // Show/hide full description
  toggleContainers = document.querySelectorAll('.short, .full')
  if (toggleContainers.length) {
    toggleContainers.forEach((element) => {
      element.firstElementChild.addEventListener('click', (event) => {
        (element.previousElementSibling || element.nextElementSibling).classList.toggle('hidden')
        element.classList.toggle('hidden')
      })
    })
  }

  // Modals close
  modals = document.querySelectorAll('.modal')
  if (modals.length) {
    modals.forEach((modal) => {
      modal.querySelectorAll('button').forEach((btn) => {
        btn.addEventListener('click', (event) => {
          modal.classList.remove('is-active')
        })
      })
    })
  }

  // Add modal open
  trigger = document.getElementById('add-trigger')
  if (trigger) {
    trigger.addEventListener('click', (event) => {
      document.getElementById('add-modal').classList.add('is-active')
    })
  }

  // Edit expense button actions
  editBtns = document.querySelectorAll('.edit-icon')
  if (editBtns.length) {
    editBtns.forEach((element) => {
      element.addEventListener('click', (event) => {
        document.getElementById('update-id').value = element.dataset.id
        document.getElementById('update-amount').value = element.dataset.amount
        document.getElementById('update-category').value = element.dataset.category
        document.getElementById('update-description').value = element.dataset.description
        document.getElementById('update-modal').classList.add('is-active')
        console.log(element.dataset.choices)
      })
    })  
  }

})
