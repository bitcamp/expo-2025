<template>
    <div class="all-content-container">
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

    img {
        width: 30%;
        margin: 4rem;
    }
}

.all-content-container {
    width: 100%;
    height: 100%;
    background-image: linear-gradient(180deg, #7C3B35, #E26F3C, #F0984C);
    flex-direction: column;
    padding-bottom: 3rem;
}

.filter-and-competitions-content {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
</style>