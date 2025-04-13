<template>
    <div class="wrapper">
        <div class="hero">
            <img src="../assets/images/background/bitcamp.svg" class="svgStyle" alt="Bitcamp sign" />
        </div>
        <div class="filter-and-competitions-content">
            <div class="filter-component">
                <!-- Pass the distinct team names & distinct challenge names to our Filter component -->
                <FilterComponent :teamNames="state.teamNames" :challengeNames="state.categoryNames" />
            </div>
            <div class="competitions-component">
                <!-- Our main container for displaying teams/projects -->
                <TeamContainer />
            </div>
        </div>
        <img src="../assets/images/TRexFossil.svg" class="right-img" alt="Dino" />
    </div>
</template>

<script setup lang="ts">
import { reactive, provide, onMounted } from 'vue'
import FilterComponent from './FilterComponent.vue'
import TeamContainer from './TeamContainer.vue'

const state = reactive({
    filteredTeamNames: [],
    filteredChallengeNames: '',
    projectType: 'all',

    // Our new data references
    teams: [],
    teamNames: [],
    categoryNames: []
})

const fetchData = async () => {
    const response = await fetch('/expo_algorithm_results.json')
    const data = await response.json()

    // 1) Keep raw array of teams
    state.teams = data

    // 2) Distinct team names
    state.teamNames = data.map((t: any) => t.team_name)

    // 3) Distinct challenge names
    const allChallenges = data.flatMap((t: any) =>
        t.challenges.map((c: any) => c.challenge_name)
    )
    state.categoryNames = [...new Set(allChallenges)]
}

onMounted(fetchData)

// Make our state globally available
provide('state', state)
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
    background-image: url('@/assets/images/background/Background.svg'), linear-gradient(#FF5D00, #E6A52D);
    background-size: 220% auto;
    background-position: center bottom;
    background-repeat: no-repeat;
    background-attachment: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    padding: 4rem 0 6.5rem;

    @media (max-width: 800px) {
        padding: 3rem 0 5rem;
        height: 135vh;
    }
}

.right-img {
    position: absolute;
    right: 0;
    bottom: 300px;
    width: 150px;
    height: auto;
    z-index: 0;
    pointer-events: none;
}

.filter-and-competitions-content {
    display: flex;
    flex-direction: row;
    justify-content: center;
    position: relative;
    z-index: 10;

    @media (max-width: 800px) {
        flex-direction: column;
        justify-content: center;
        align-content: center;
        flex-wrap: wrap;
    }
}
</style>