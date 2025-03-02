import Alpine from 'alpinejs'
 
window.Alpine = Alpine

document.addEventListener('alpine:init', () => {

    const leftSide = document.querySelector('.left-side')
    leftSide.style.transition = 'left 0.3s ease-out'

    Alpine.data('layout', () => ({

        openLeftSide() {
            leftSide.style.left = '0'
        },
        closeLeftSide() {
            leftSide.style.left = 'calc(var(--left-side-w)* -1)'
        },
    }))
})

Alpine.start()
