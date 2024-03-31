<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="table-header">{{ teamDetails[0][0] }}</div>
            <div class="project-info-container">
                <div class="project-header"> {{ teamDetails[0][1] }}</div>
                <button class="challenges-button" @click="toggleButton">
                    <div class="button-text">
                        show challenges
                    </div>
                    <img src="../assets/images/openChallengesArrow.svg" class="arrow-image"
                        :class="{ 'arrow-right': !showChallenges, 'arrow-down': showChallenges }" alt="Bitcamp sign" />
                </button>

                <div :class="{ 'challenges-hidden': !showChallenges, 'challenges-shown': showChallenges }">
                    <JudgingRow categoryName="deez" companyName="nutz" judgeName="69" timing="times" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const showChallenges = ref<Boolean>();
function toggleButton() {
    if (showChallenges.value === true) {
        showChallenges.value = false;
    } else {
        showChallenges.value = true;
    }
}

const props = defineProps({
    teamDetails: {
        type: Array,
        required: true,
    },
});
</script>
<style scoped lang="scss">
.entire-container {
    background-color: #F6EBCC;
    border-radius: 2rem;
}

.top-row {
    display: flex;
    flex-direction: row;
    padding: 1rem;
}

.project-info-container {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    position: relative;
    flex-grow: 1;
}

.table-header {
    font-size: 1.5rem;
    width: 6rem;
    text-align: center;
    color: #FFC226;
}

.project-header {
    font-size: 1.5rem;
    color: #E34E30;
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
}

.challenges-hidden {
    display: none;
}

.challenges-shown {
    display: flex;
    width: 100%;
}

.button-text {
    justify-content: center;
    align-content: center;
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