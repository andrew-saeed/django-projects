import Alpine from 'alpinejs'
 
window.Alpine = Alpine

document.addEventListener('alpine:init', () => {

    const leftSide = document.querySelector('.left-side')
    leftSide.style.transition = 'left 0.3s ease-out'

    Alpine.data('profile', () => ({
        init() {
            this.$refs.photoInput.addEventListener('change', (e) => {
                const file = e.target.files[0]
                if(file) {
                    const reader = new FileReader()
                    reader.onload = (e) => {
                        this.$refs.photoImg.src = e.target.result
                    }
                    reader.readAsDataURL(file)
                }
            })
        },
        openPhotoImgInput() {
            this.$refs.photoInput.click()
        }
    }))

    Alpine.data('layout', () => ({

        dropmask: false,
        accountDropdownOpen: false,

        openLeftSide() {
            leftSide.style.left = '0'
            this.dropmask = true
        },
        closeLeftSide() {
            leftSide.style.left = 'calc(var(--left-side-w)* -1)'
            this.dropmask = false
        },
        toggleAccountDropdown() {
            this.accountDropdownOpen = !this.accountDropdownOpen
        }
    }))
})

Alpine.start()
