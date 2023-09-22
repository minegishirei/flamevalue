

<template>
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Products | RedStore</title>
        <link rel="stylesheet" href="style.css">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
            rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>

    <body>
        <MyHeader></MyHeader>

        <!-- Single Products -->
        <div class="small-container single-product">
            <FullCalendar :options="calendarOptions" />

        </div>
        <!-- title -->
        <div class="small-container">
            <div class="row row-2">
                <h2>Related Products</h2>
                <p>View More</p>
            </div>
        </div>

        <div class="categories">
            <div class="small-container">
                <div class="row">
                    <div class="col-4" v-for="(item, key) in store_top4" :key="key">
                        <a v-bind:href="`product_details.html?id=${item.id}`">
                            <img v-bind:src="`${item.images[1] ? item.images[1] : item.images[0]}`">
                        </a>
                        <h4>{{ item.title }}</h4>

                        <p>{{ item.date }}</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- Footer -->
        <div class="footer">
            <div class="container">
                <div class="row">
                    <div class="footer-col-1">
                        <h3>Download Our App</h3>
                        <p>Download App for Android and ios mobile phone.</p>
                        <div class="app-logo">
                            <img src="images/play-store.png">
                            <img src="images/app-store.png">
                        </div>
                    </div>
                    <div class="footer-col-2">
                        <img src="images/logo-white.png">
                        <p>Our Purpose Is To Sustainably Make the Pleasure and Benefits of Sports Accessible to the Many.
                        </p>
                    </div>
                    <div class="footer-col-3">
                        <h3>Useful Links</h3>
                        <ul>
                            <li>Coupons</li>
                            <li>Blog Post</li>
                            <li>Return Policy</li>
                            <li>Join Affiliate</li>
                        </ul>
                    </div>
                    <div class="footer-col-4">
                        <h3>Follow Us</h3>
                        <ul>
                            <li>Facebook</li>
                            <li>Twitter</li>
                            <li>Instagram</li>
                            <li>Youtube</li>
                        </ul>
                    </div>
                </div>
                <hr>
                <p class="copyright">Copyright 2020 - Samwit Adhikary</p>
            </div>
        </div>

        <!-- javascript -->
        <component :is="'script'">
            var MenuItems = document.getElementById("MenuItems");
            MenuItems.style.maxHeight = "0px";
            function menutoggle() {
            if (MenuItems.style.maxHeight == "0px") {
            MenuItems.style.maxHeight = "200px"
            }
            else {
            MenuItems.style.maxHeight = "0px"
            }
            }
        </component>
        <!-- product gallery -->

        <component :is="'script'">
            var ProductImg = document.getElementById("ProductImg");
            var SmallImg = document.getElementsByClassName("small-img");

            SmallImg[0].onclick = function () {
            ProductImg.src = SmallImg[0].src;
            }
            SmallImg[1].onclick = function () {
            ProductImg.src = SmallImg[1].src;
            }
            SmallImg[2].onclick = function () {
            ProductImg.src = SmallImg[2].src;
            }
            SmallImg[3].onclick = function () {
            ProductImg.src = SmallImg[3].src;
            }
        </component>
    </body>

    </html>
</template>

<script>
import store from "../store/store";
import MyHeader from "./molcutes/MyHeader";

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
//import interactionPlugin from '@fullcalendar/interaction'
import FullCalendarInteraction from '@fullcalendar/interaction';

export default {
    name: 'WakouProductDetails',
    data() {
        document.title = "和光市のイベントをカレンダーから探す!"
        return Object.assign(
            {
                store: store,
                store_top4: Object.fromEntries(Object.entries(store).slice(0, 4)),
                calendarOptions: {
                    plugins: [dayGridPlugin, FullCalendarInteraction],
                    headerToolbar: {
                        left: '',
                        center: 'title',
                        right: 'prev,next'
                    },
                    locale: 'ja',
                    initialView: 'dayGridMonth',
                    dateClick: this.handleDateClick,
                    eventClick: this.handleEventClick,
                    events: Object.values(store).map(row => Object.assign({
                        title: row.title,
                        date: row.split_date[0] + "-" + String(row.split_date[1]).padStart(2, '0') + "-" + row.split_date[2],
                        id : row.id
                    }))

                }
            })
    },
    components: {
        'MyHeader': MyHeader,
        'FullCalendar': FullCalendar // make the <FullCalendar> tag available
    },
    methods: {
        handleDateClick: function () {
        },
        handleEventClick: function (arg) {
            console.log(arg)
            console.log(arg.event._def.publicId)
            window.location.href = `./product_details.html?id=${ arg.event._def.publicId}`
        }
    }
}

</script>
