<template>
    <div class="entire-container" v-for="(teamDetail, index) in teamDetails" :key="index">
        <div class="top-row" v-if="filtered.includes(teamDetail[1]) && (challengeDetails === '' || teamDetail[2].some(challenge => challengeDetails.includes(challenge[0]))) &&
        (projectType === 'all' ||
            (projectType === 'virtual' && teamDetail[0] === 'virtual') ||
            (projectType === 'in-person' && teamDetail[0] !== 'virtual'))">
            <div v-if="teamDetail[0] !== 'virtual'" class="table-header">{{ teamDetail[0] }}</div>
            <div v-if="teamDetail[0] === 'virtual'" class="table-header">
                <img src="../assets/images/filmCamera.svg" class="camera-style">
            </div>
            <div class="project-info-container">
                <div class="button-container">
                    <div class="project-header"> {{ teamDetail[1] }}</div>
                    <button v-if="windowWidth > 800 && challengeDetails === ''" class="challenges-button"
                        @click="toggleButton(teamDetail[1])">
                        <div class="button-text">
                            show challenges
                        </div>
                        <img src="../assets/images/openChallengesArrow.svg" class="arrow-image-small"
                            :class="{ 'arrow-right': !showChallenges.includes(teamDetail[1]), 'arrow-down': showChallenges.includes(teamDetail[1]) }"
                            alt="Bitcamp sign" />

                    </button>
                    <button v-if="windowWidth < 800 && challengeDetails === ''" class="challenges-button-large"
                        @click="toggleButton(teamDetail[1])">
                        <img src="../assets/images/openChallengesArrowLarge.svg" class="arrow-image-large"
                            :class="{ 'arrow-right': !showChallenges.includes(teamDetail[1]), 'arrow-down': showChallenges.includes(teamDetail[1]) }"
                            alt="Bitcamp sign" />

                    </button>
                </div>
                <div v-if="challengeDetails === ''"
                    :class="{ 'challenges-hidden': !showChallenges.includes(teamDetail[1]), 'challenges-shown': showChallenges.includes(teamDetail[1]) }">
                    <JudgingRow v-for="(challenge, challengeIndex) in teamDetail[2]"
                        :key="`challenge-${index}-${challengeIndex}`" :categoryName="challenge[0]"
                        :companyName="challenge[1]" :judgeName="challenge[2]" :timing="challenge[3]" />
                </div>
                <div v-if="challengeDetails !== ''" class="challenges-shown">
                    <JudgingRow
                        v-for="(challenge, challengeIndex) in teamDetail[2].filter(challenge => challengeDetails.includes(challenge[0]))"
                        :key="`challenge-${index}-${challengeIndex}`" :categoryName="challenge[0]"
                        :companyName="challenge[1]" :judgeName="challenge[2]" :timing="challenge[3]" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';

const showChallenges = ref<string[]>([]);
const windowWidth = ref(0);

const toggleStates = ref([]);

function toggleButton(name: string) {
    const index = showChallenges.value.indexOf(name);
    if (index !== -1) {
        showChallenges.value.splice(index, 1);
        toggleStates.value[index] = false;
    } else {
        showChallenges.value.push(name);
        const teamIndex = props.teamDetails.findIndex(team => team[1] === name);
        if (teamIndex !== -1) {
            toggleStates.value[teamIndex] = true;
        }
    }
}

const updateWindowWidth = () => {
    windowWidth.value = window.innerWidth;
};

onMounted(() => {
    updateWindowWidth();
    window.addEventListener('resize', updateWindowWidth);
    toggleStates.value = props.teamDetails.map(team => showChallenges.value.includes(team[1]));
});

onUnmounted(() => {
    window.removeEventListener('resize', updateWindowWidth);
});

const props = defineProps({
    filtered: {
        type: Array,
        required: true,
    },
    teamDetails: {
        type: Array,
        required: true,
    },
    challengeDetails: {
        type: Array,
        required: true,
    },
    projectType: {
        type: Array,
        required: true,
    },
});

watch([() => props.filtered, () => props.challengeDetails, () => props.projectType], () => {
    showChallenges.value = [];
}, { deep: true });
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
    min-width: 100px;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: center;

    @media (max-width: 800px) {
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

.challenges-button-large {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    flex-direction: row;
    width: fit-content;
    font-family: 'Inter';
    color: #FF8F28;
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

.camera-style {
    width: 1.5rem;
}

.button-container {
    display: flex;
    flex-direction: column;

    @media (max-width: 800px) {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
}

.toggle-size {
    transform: scale(0.8);
    transform-origin: center;
}

.button-text {
    align-content: center;
    justify-content: space-evenly;
}

.arrow-image-small {
    margin-inline: 0.35rem;
    width: 0.69rem;
    transition: transform 0.3s ease;
}

.arrow-image-large {
    margin-inline: 0.35rem;
    width: 1rem;
    transition: transform 0.2s ease;
    color: #FF8F28;
}

.arrow-right {
    transform: rotate(0deg);
}

.arrow-down {
    transform: rotate(90deg);
}

.arrow-half {
    transform: rotate(45deg);
}
</style>