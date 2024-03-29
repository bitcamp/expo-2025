<template>
    <div class="hero-wrapper">      
        <div class="hero">
            <img
          src="../assets/images/background/HeroSign.svg"
          class="svgStyle"
          alt="Bitcamp sign"
        />
    </div>
    </div>
</template>  

<script setup lang="ts">  
</script>

<style scoped lang="scss">

.hero {
    position: absolute;
    background-image: linear-gradient(180deg, #7C3B35, #E26F3C, #F0984C);
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;

    img{
        width: 100%;
    }
}
</style>