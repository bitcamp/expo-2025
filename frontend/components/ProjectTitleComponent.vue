<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="table-header">AI</div>
            <div class="project-info-container">
                <div class="project-header">Project</div>
                <button class="challenges-button" @click="toggleButton">
                    show challenges
                </button>

                <div :class="{ 'challenges-hidden': !showChallenges, 'challenges-shown': showChallenges }">
                    deez
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

</script>

<style lang="scss">
.entire-container {
    background-color: #F6EBCC;
    border-radius: 2rem;
    padding: 3rem;
}

.top-row {
    display: flex;
    flex-direction: row;
}

.project-info-container {
    height: 5rem;
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    padding-inline: 1rem;
}

.table-header {
    font-size: 1.5rem;
    margin-inline: 1rem;
}

.project-header {
    font-size: 1.5rem;
}

.challenges-button {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
}

.challenges-hidden {
    display: none;
}

.challenges-shown {
    display: inline;
}
</style>