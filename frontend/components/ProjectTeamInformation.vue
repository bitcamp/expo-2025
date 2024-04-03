<template>
    <div class="entire-container" v-for="(teamDetail, index) in teamDetails" :key="index">
        <div class="top-row" v-if="filtered.includes(teamDetail[1])">
            <div class="table-header">{{ teamDetail[0] }}</div>
            <div class="project-info-container">
                <div class="project-header"> {{ teamDetail[1] }}</div>
                <button class="challenges-button" @click="toggleButton(teamDetail[1])">
                    <div class="button-text">
                        show challenges
                    </div>
                    <img src="../assets/images/openChallengesArrow.svg" class="arrow-image"
                        :class="{ 'arrow-right': !showChallenges.includes(teamDetail[1]), 'arrow-down': showChallenges.includes(teamDetail[1]) }"
                        alt="Bitcamp sign" />
                </button>
                <div
                    :class="{ 'challenges-hidden': !showChallenges.includes(teamDetail[1]), 'challenges-shown': showChallenges.includes(teamDetail[1]) }">
                    <JudgingRow v-for="(challenge, challengeIndex) in teamDetail[2]"
                        :key="`challenge-${index}-${challengeIndex}`" :categoryName="challenge[0]"
                        :companyName="challenge[1]" :judgeName="challenge[2]" :timing="challenge[3]" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const showChallenges = ref<string[]>([]);
function toggleButton(name: string) {
    const index = showChallenges.value.indexOf(name);
    if (index !== -1) {
        showChallenges.value.splice(index, 1);
    } else {
        showChallenges.value.push(name);
    }
}

const props = defineProps({
    filtered: {
        type: Array,
        required: true,
    },
    teamDetails: {
        type: Array,
        required: true,
    },
});


console.log("filtered" + props.filtered);

</script>
<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');
.entire-container {
    background-color: #F6EBCC;
    border-radius: 2rem;
}

.top-row {
    display: flex;
    flex-direction: row;
    padding: 1rem 0 0;
    margin-inline: 2rem;
}

.project-info-container {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    position: relative;
    flex-grow: 1;
    color: #484241;
}

.table-header {
    font-size: 1.5rem;
    width: 6rem;
    margin-right: 2rem;
    text-align: center;
    color: #FFC226;
    font-family: 'Aleo';

    @media (max-width: 800px) {
      text-align: left;
      margin-right: 0;
    }
}

.project-header {
    font-size: 1.5rem;
    color: #E34E30;
    font-family: 'Aleo';
}

.challenges-button {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
    text-align: left;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    display: flex;
    flex-direction: row;
    width: fit-content;
    font-family: 'Inter';
    color: #A49B83;
}

.challenges-hidden {
    display: none;
}

.challenges-shown {
    display: flex;
    flex-direction: column;
    width: 100%;
    font-family: 'Inter';
}

.button-text {
    align-content: center;
    justify-content: space-evenly;
  }

.arrow-image {
    margin-inline: 0.35rem;
    width: 0.69rem;
    transition: transform 0.3s ease;
}

.arrow-right {
    transform: rotate(0deg);
}

.arrow-down {
    transform: rotate(90deg);
}
</style>