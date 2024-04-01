<template>
    <div class="wrapper">      
        <div class="hero">
            <img src="../assets/images/background/HeroSign.svg" class="svgStyle" alt="Bitcamp sign" />      
        </div>
        <div class="filter-and-competitions-content">
            <div class="filter-component">
                <FilterComponent :challengeName="['LA', 'BS']" />
            </div>
            <div class="competitions-component">
                <ProjectComponent />
            </div>
        </div>
    </div>
    
</template>  

<script setup lang="ts">  
import FilterComponent from "./FilterComponent.vue";
import ProjectComponent from "./ProjectComponent.vue";
</script>

<style scoped lang="scss">
.hero {
    display: flex;
    justify-content: center;
    margin-bottom: 3rem;

    img {
        width: 25%;
        min-width: 20rem;
    }
}

.wrapper {
    position: absolute;
    background-image: linear-gradient(180deg, #7C3B35, #E26F3C, #F0984C);
    top: 0;
    left: 0; 
    width: 100%;
    height: 100vh;
    padding: 4rem 0 7rem;
}

.filter-and-competitions-content {
    
    display: flex;
    flex-direction: row;
    justify-content: center;   
}
</style>

