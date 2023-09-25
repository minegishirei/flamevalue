<template>
  <!-- Header -->
  <div class="px-4 md:px-10 mx-auto w-full">
    <div>
      <div class="flex flex-wrap">
        <div class="lg:w-2/12 xl:w-2/12 px-12 pb-12 ">
          <div style="color: white;">
            <p style="font-size: 25px;">{{ title }}</p>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap">
        <div class="lg:w-2/12 xl:w-2/12 px-4 pt-8">
          <img :src="`${image}`" style="width: 130px; ">
        </div>
        <div class="lg:w-8/12 xl:w-8/12 px-4 pt-6">
          <div style="color: white;">
            {{ explain }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LangInfo from '/static/flamevalue/Java.json';

export default {
  data() {
    return LangInfo
  }
};
</script>
