<template>
<!DOCTYPE html>
<html lang="ja">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <!-- Meta, title, CSS, favicons, etc. -->
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png" rel="icon">
  <script src="https://code.jquery.com/jquery-3.6.1.slim.min.js"></script>

  <!-- TWITTER -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@se_maintain">
  <meta name="twitter:creator" content="@se_maintain">
  <meta name="twitter:title" content="{{ title }}">
  <meta name="twitter:description" content="{{ description }}">

  <meta name="twitter:image" content="{{ img }}">

  <meta name="twitter:image"
    content="https://question.short-tips.info/api/ogp/?text={{ name }}...score {{ stars }} {{ total_score }} ......平均下限年収 : {{ basic.money }}万円...平均上限年収 : {{ basic.overtime }}万円...総求人数 : {{ basic.count }}件...リモート率 : {{ basic.remote }}％...Qiitaタグ数 : {{ basic.qiita_score }}件 .........{{ title }}">

  <title>{{ title }}</title>
  <meta name="description" content="{{ description }}">

</head>


<body class="nav-md">
  <div class="container body">
    <div class="main_container">
      <!-- top navigation -->
      <div class="top_nav" style="margin-left: 0px; ">
        <div class="nav_menu" style="background-color: #2A3F54; margin-bottom: 0;">
          <div class="main_contents" style="background-color: #2A3F54;">

            <div class="nav toggle">
              <ul class=" navbar-right" style="padding-left: 0px;">

                <li class="nav-item dropdown open" style="padding-left: 0px;">
                  <a href="/" class="user-profile dropdown-toggle" aria-haspopup="true" id="navbarDropdown"
                    data-toggle="dropdown" aria-expanded="false">
                    <img src="https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png" alt="">
                    <n style=" color: white;">flamevalue</n>
                  </a>
                </li>


              </ul>
            </div>

            <nav class="nav navbar-nav">
              <ul class=" navbar-right">

                <span id="js_hidden">
                  <li class="nav-item dropdown open only_pc">
                    <a href="https://twitter.com/se_maintain" class="user-profile dropdown-toggle" aria-haspopup="true"
                      id="navbarDropdown" data-toggle="dropdown" aria-expanded="false">
                      <img src="/static/jobstatic/img/color.png" alt="">
                      <n style=" color: white;">問い合わせ</n>
                    </a>
                  </li>

                  <li class="nav-item dropdown open only_pc">
                    <div class="search_container" style="background-color: white;" onsubmit="transition()">
                      <input type="text" size="40" placeholder="キーワード検索" id="query_text_box" list="candidate_list"
                        autocomplete="off">
                      <datalist id="candidate_list">
                      </datalist>
                      <input type="submit"  onclick="transition()">
                    </div>
                  </li>

                  <li class="nav-item dropdown open only_pc">
                    <a href="/ranking.html" class="user-profile dropdown-toggle" aria-haspopup="true"
                      id="navbarDropdown" data-toggle="dropdown" aria-expanded="false">
                      <n style=" color: white;">開発言語ランキング</n>
                      <img src="/static/jobstatic/img/color.png" alt="">
                    </a>
                  </li>
                </span>







              </ul>

            </nav>


          </div>

          <div class="nav-item dropdown open only_mobile" style="padding: 10px;">
            <div class="search_container" style="background-color: white;" onsubmit="transition()">
              <input type="text" size="50" placeholder="キーワード検索" id="query_text_box" list="candidate_list"
                autocomplete="off">
              <datalist id="candidate_list">
              </datalist>
              <input type="submit"  onclick="transition()">
            </div>
          </div>


        </div>



      </div>
      <!-- /top navigation -->

      <BodyComponent />

      {% block content %}
      {% endblock %}


      <!-- footer content -->
      <footer style="margin-left: 0px; ">
        <div class="pull-right">
          Gentelella - Bootstrap Admin Template by <a href="https://colorlib.com">Colorlib</a>
        </div>
        <div class="clearfix"></div>
      </footer>
      <!-- /footer content -->
    </div>
  </div>



</body>

</html>





</template>


<style>
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

input::-webkit-calendar-picker-indicator {
  display: none;
}

.search_container {
  box-sizing: border-box;
  position: relative;
  border: 1px solid #999;
  padding-left: 10px;
  border-radius: 5px;
  height: 2.5em;
  width: 100%;
  overflow: hidden;
}

.search_container input[type="text"] {
  border: none;
  height: 2.5em;
}

.search_container input[type="text"]:focus {
  outline: 0;
}

.search_container input[type="submit"] {
  cursor: pointer;
  font-family: FontAwesome;
  font-size: 1.3em;
  border: none;
  background: none;
  color: #3879D9;
  position: absolute;
  width: 2.5em;
  height: 3.0em;
  right: 0;
  top: -10px;
  outline: none;
}

input::-webkit-calendar-picker-indicator {
  display: none;
}
</style>


<style>


  .main_contents {
    background-color: #f8f9fa;
  }

  .main_contents {
    background-color: #f8f9fa;
  }

  @media screen and (min-width: 680px) {
    .main_contents {
      background-color: #f8f9fa;
      padding-left: 15%;
      padding-right: 15%;
    }
  }
</style>

<style>
@import "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css";
@import "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";
</style>

<style>
@media screen and (max-width:767px) {
  .only_pc {
    display: none;
  }
}

@media screen and (min-width:767px) {
  .only_mobile {
    display: none;
  }
}
</style>

<style>
.dropdown-toggle::after {
  content: initial;
}
</style>



<script>
import BodyComponent from "./BodyComponent.vue";
export default {
    name: 'MyTemplate',
    data() {
        return Object.assign({
            title: "タイトル"
        })
    },
    components:{
        BodyComponent
    }
}

</script>
