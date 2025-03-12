import flatpickr from "flatpickr"
import Alpine from 'alpinejs'
 
window.Alpine = Alpine

import 'flatpickr/dist/flatpickr.css'
import 'flatpickr/dist/themes/dark.css'

document.addEventListener('alpine:init', () => {

    const leftSide = document.querySelector('.left-side')
    leftSide.style.transition = 'left 0.3s ease-out'

    Alpine.data('postsList', () => ({

        page:1,
        isFetching: false,
        emptyPage: false,

        init() {
            window.addEventListener('scroll', () => {
                const margin = document.body.clientHeight - window.innerHeight - 200;
                if(window.scrollY > margin && !this.emptyPage && !this.isFetching) {
                    this.fetchPosts()
                }
            })
        },
        async fetchPosts() {
            this.page++
            this.isFetching = true
            const res = await fetch(`?list-paginated=1&page=${this.page}`)
            const html = await res.text()
            if(html === '') this.emptyPage = true
            this.$el.querySelector('ul').insertAdjacentHTML('beforeend', html)
            this.isFetching = false
        }
    }))

    Alpine.data('profile', () => ({
        init() {
            flatpickr("#id_date_of_birth", {})

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
        headerDropdownOpen: false,

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
        },
        toggleHeaderDropdown() {
            this.headerDropdownOpen = !this.headerDropdownOpen
        }
    }))
})

Alpine.start()
