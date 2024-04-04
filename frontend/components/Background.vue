<template>
    <div class="wrapper">
        <div class="hero">
            <img src="../assets/images/background/HeroSign.svg" class="svgStyle" alt="Bitcamp sign" />
        </div>
        <div class="filter-and-competitions-content">
            <div class="filter-component">
                <FilterComponent :teamNames="['Lakers', 'Clippers', 'Grizzlies', 'Cavs']"
                    :challengeNames="['deez', 'doze', 'your', 'everyone']" />
            </div>
            <div class="competitions-component">
                <TeamContainer />
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { reactive, provide } from 'vue';
import FilterComponent from "./FilterComponent.vue";
import TeamContainer from "./TeamContainer.vue";

const state = reactive({
    filteredTeamNames: [],
    filteredChallengeNames: "",
    projectType: "",
});

provide('state', state);
</script>

<style scoped lang="scss">
.hero {
    display: flex;
    justify-content: center;
    margin-bottom: 4rem;

    img {
        width: 30%;
        min-width: 20rem;
    }
}

.wrapper {
    position: absolute;
    background-image: linear-gradient(180deg, #7C3B35, #E26F3C, #F0984C);
    top: 0;
    left: 0;
    width: 100%;
    height: 110vh;
    padding: 4rem 0 7rem;

    @media (max-width: 800px) {
        padding: 3rem 0 7rem;
        height: 175vh;
    }
}

.filter-and-competitions-content {
    display: flex;
    flex-direction: row;
    justify-content: center;

    @media (max-width: 800px) {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-content: center;
        flex-wrap: wrap;
    }
}
</style>
