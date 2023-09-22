
<template>
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RedStore | Ecommerce Website Design</title>
        <link rel="stylesheet" href="style.css">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
            rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>

    <body>

        <MyHeader></MyHeader>
        <!-- Feadtued Categories -->

        <div class="categories">
            <h2 class="title">注目イベント</h2>
            <div class="small-container">
                <div class="row">
                    <div class="col-3" v-for="(item, key) in store_top3" :key="key">
                        <a v-bind:href="`product_details.html?id=${item.id}`">
                            <img v-bind:src="`${item.images[1]? item.images[1] : item.images[0]}`">
                        </a>
                        <h4>{{ item.title }}</h4>

                        <p>{{ item.date }}</p>
                    </div>
                </div>
            </div>
        </div>


        <!-- Featured Products -->

        <div class="small-container">
            <h2 class="title">近日開催予定イベント!</h2>
            <div class="row">
                <div class="col-4" v-for="(item, key) in store_after3" :key="key">
                    <a v-bind:href="`product_details.html?id=${item.id}`">
                        <img v-bind:src="`${item.images[1]? item.images[1] : item.images[0]}`">
                    </a>
                    <h4>{{ item.title }}</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>{{ item.date }}</p>
                </div>
            </div>
        </div>
        <!-- Offer -->
        <div class="offer">
            <div class="small-container">
                <div class="row">
                    <div class="col-2">
                        <img src="images/exclusive.png" class="offer-img">
                    </div>
                    <div class="col-2">
                        <p>Exclusively Available on RedStore</p>
                        <h1>Smart Band 4</h1>
                        <small>The Mi Smart Band 4 fearures a 39.9%larger (than Mi Band 3) AMOLED color full-touch display
                            with adjustable brightness, so everything is clear as can be.<br></small>
                        <a href="products.html" class="btn">Buy Now &#8594;</a>
                    </div>
                </div>
            </div>
        </div>


        <div class="small-container">
            <h2 class="title">Latest Products</h2>
            <div class="row">
                <div class="col-4">
                    <img src="images/product-5.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-6.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-7.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-8.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
            </div>
            <div class="row">
                <div class="col-4">
                    <img src="images/product-9.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-10.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-11.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
                <div class="col-4">
                    <img src="images/product-12.jpg">
                    <h4>Red Printed T-Shirt</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$50.00</p>
                </div>
            </div>
        </div>

        <!-- Offer -->
        <div class="offer">
            <div class="small-container">
                <div class="row">
                    <div class="col-2">
                        <img src="images/exclusive.png" class="offer-img">
                    </div>
                    <div class="col-2">
                        <p>Exclusively Available on RedStore</p>
                        <h1>Smart Band 4</h1>
                        <small>The Mi Smart Band 4 fearures a 39.9%larger (than Mi Band 3) AMOLED color full-touch display
                            with adjustable brightness, so everything is clear as can be.<br></small>
                        <a href="products.html" class="btn">Buy Now &#8594;</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Testimonial -->
        <div class="testimonial">
            <div class="small-container">
                <div class="row">
                    <div class="col-3">
                        <i class="fa fa-quote-left"></i>
                        <p>Lorem ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been
                            industry's standard dummy text.</p>
                        <div class="rating">
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                        </div>
                        <img src="images/user-1.png">
                        <h3>Sean Parker</h3>
                    </div>
                    <div class="col-3">
                        <i class="fa fa-quote-left"></i>
                        <p>Lorem ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been
                            industry's standard dummy text.</p>
                        <div class="rating">
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                        </div>
                        <img src="images/user-2.png">
                        <h3>Mike Smith</h3>
                    </div>
                    <div class="col-3">
                        <i class="fa fa-quote-left"></i>
                        <p>Lorem ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been
                            industry's standard dummy text.</p>
                        <div class="rating">
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                        </div>
                        <img src="images/user-3.png">
                        <h3>Mabel Joe</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Brands -->

        <div class="brands">
            <div class="small-container">
                <div class="row">
                    <div class="col-5">
                        <img src="images/logo-godrej.png">
                    </div>
                    <div class="col-5">
                        <img src="images/logo-oppo.png">
                    </div>
                    <div class="col-5">
                        <img src="images/logo-coca-cola.png">
                    </div>
                    <div class="col-5">
                        <img src="images/logo-paypal.png">
                    </div>
                    <div class="col-5">
                        <img src="images/logo-philips.png">
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
    </body>

    </html>
</template>

<script>

import MyHeader from "./molcutes/MyIndexHeader";
import store from "../store/store";
export default {
    name: 'WakouIndex',
    data() {
        document.title = "和光イベントカレンダー ~和光市で開催されるイベント一覧~"
        return {
            store_top3: Object.fromEntries(Object.entries(store).slice(0, 3)),
            store_after3: Object.fromEntries(Object.entries(store).slice(3,)),
            store: store
        }
    },
    components: {
        'MyHeader' : MyHeader
    }
}
</script>