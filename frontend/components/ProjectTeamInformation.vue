<template>
    <div class="entire-container">
        <!-- For each team in sorted order -->
        <div v-for="(team, index) in sortedTeamDetails" :key="team.id">
            <!-- We'll only show if the user’s text-filter includes team_name,
             the challenge filter is satisfied, and projectType is satisfied.
             That logic is already in your parent, so typically everything here
             is guaranteed to pass. You can do a final check if you'd like. -->
            <div class="top-row" v-if="
                filtered.includes(team.team_name) &&
                (challengeDetails === '' || team.challenges.some(ch => challengeDetails.includes(ch.challenge_name))) &&
                (projectType === 'all' ||
                    (projectType === 'virtual' && team.in_person === false) ||
                    (projectType === 'in-person' && team.in_person === true))
            ">
                <!-- If in-person, show table number; if not in-person, show camera icon. -->
                <div v-if="team.in_person" class="table-header">
                    {{ team.table }}
                </div>
                <div v-else class="table-header">
                    <img src="../assets/images/filmCamera.svg" class="camera-style" />
                </div>

                <div class="project-info-container">
                    <div class="button-container">
                        <!-- Link to Devpost, or wherever. -->
                        <a :href="team.link" target="_blank" class="team-url-style">
                            <div class="project-header">{{ team.team_name }}</div>
                        </a>

                        <!-- Toggle the challenges drop-down (for wide screens) -->
                        <button v-if="windowWidth > 800 && challengeDetails === ''" class="challenges-button"
                            @click="toggleButton(team.id)">
                            <div class="button-text">show challenges</div>
                            <div class="image-container">
                                <img src="../assets/images/openChallengesArrow.svg" class="arrow-image-small" :class="{
                                    'arrow-right': !showChallenges.includes(team.id),
                                    'arrow-down': showChallenges.includes(team.id)
                                }" alt="open" />
                            </div>
                        </button>

                        <!-- For smaller screens, just a bigger arrow icon -->
                        <button v-if="windowWidth < 800 && challengeDetails === ''" class="challenges-button-large"
                            @click="toggleButton(team.id)">
                            <img src="../assets/images/openChallengesArrowLarge.svg" class="arrow-image-large" :class="{
                                'arrow-right': !showChallenges.includes(team.id),
                                'arrow-down': showChallenges.includes(team.id)
                            }" alt="open" />
                        </button>
                    </div>

                    <!-- Show "No Challenges Selected" if team has no challenges at all -->
                    <div v-if="team.challenges.length === 0" :class="{
                        'no-challenges-hidden': !showChallenges.includes(team.id),
                        'no-challenges-shown': showChallenges.includes(team.id)
                    }">
                        No Challenges Selected
                    </div>

                    <!-- If no specific filter challenge is selected, show entire list (conditionally hidden) -->
                    <div v-if="challengeDetails === ''" :class="{
                        'challenges-hidden': !showChallenges.includes(team.id),
                        'challenges-shown': showChallenges.includes(team.id)
                    }">
                        <JudgingRow v-for="(challenge, challengeIndex) in team.challenges" :key="challengeIndex"
                            :categoryName="challenge.challenge_name"
                            :companyName="challenge.is_mlh ? 'Major League Hacking' : challenge.company"
                            :judgeName="challenge.judge" :startTime="challenge.start_time" :isMLH="challenge.is_mlh" />
                    </div>

                    <!-- If the user specifically picked a challenge name in filter,
                 show only that challenge for each team. -->
                    <div v-if="challengeDetails !== ''" class="challenges-shown">
                        <JudgingRow
                            v-for="(challenge, chIndex) in team.challenges.filter(ch => challengeDetails.includes(ch.challenge_name))"
                            :key="chIndex" :categoryName="challenge.challenge_name"
                            :companyName="challenge.is_mlh ? 'Major League Hacking' : challenge.company"
                            :judgeName="challenge.judge" :startTime="challenge.start_time" :isMLH="challenge.is_mlh" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import JudgingRow from './JudgingRow.vue'

interface Team {
    id: string
    team_name: string
    in_person: boolean
    table: string
    link: string
    challenges: Array<{
        is_mlh: boolean
        challenge_name: string
        company: string
        judge: string
        start_time: string
    }>
}

// props from the parent
const props = defineProps<{
    filtered: string[]
    teamDetails: Team[]
    challengeDetails: string
    projectType: string
}>()

// keep track of which team’s challenges are “expanded”
const showChallenges = ref<string[]>([])
const windowWidth = ref<number>(0)

// sort teams if the user has chosen a specific challenge
const sortedTeamDetails = computed<Team[]>(() => {
    // if no particular challenge filter, just return as is
    if (props.challengeDetails === '') {
        return props.teamDetails
    }

    // Otherwise sort by the start_time of the chosen challenge (earliest first)
    return [...props.teamDetails].sort((a, b) => {
        const aChallenge = a.challenges.find(ch => ch.challenge_name === props.challengeDetails)
        const bChallenge = b.challenges.find(ch => ch.challenge_name === props.challengeDetails)

        // If either does not have it, put them at the bottom
        if (!aChallenge && !bChallenge) return 0
        if (!aChallenge) return 1
        if (!bChallenge) return -1

        // Compare times
        const aTime = aChallenge.start_time ? Date.parse(aChallenge.start_time) : Infinity
        const bTime = bChallenge.start_time ? Date.parse(bChallenge.start_time) : Infinity
        return aTime - bTime
    })
})

function toggleButton(teamId: string) {
    const index = showChallenges.value.indexOf(teamId)
    if (index !== -1) {
        showChallenges.value.splice(index, 1)
    } else {
        showChallenges.value.push(teamId)
    }
}

const updateWindowWidth = () => {
    windowWidth.value = window.innerWidth
}

onMounted(() => {
    updateWindowWidth()
    window.addEventListener('resize', updateWindowWidth)
})

onUnmounted(() => {
    window.removeEventListener('resize', updateWindowWidth)
})

// If the user changes filters, close all open expansions
watch(
    [() => props.filtered, () => props.challengeDetails, () => props.projectType],
    () => {
        showChallenges.value = []
    },
    { deep: true }
)

</script>

<style scoped lang="scss">
.entire-container {
    background-color: #f6ebcc;
    border-radius: 2rem;
}

.top-row {
    display: flex;
    flex-direction: row;
    padding: 1rem 0 0;
    margin-inline: 1.25rem;

    @media (max-width: 800px) {
        display: inline-block;
        padding: 3rem 0 0 calc(10vw - 2.5rem);
    }
}

.project-info-container {
    display: flex;
    flex-direction: column;
    position: relative;
    flex-grow: 1;
    color: #484241;

    @media (max-width: 800px) {
        align-items: center;
    }
}

.table-header {
    font-size: 1.5rem;
    width: 4rem;
    margin-right: 1.5rem;
    text-align: center;
    color: #ff3e00;
    font-family: 'Aleo';
    min-width: 100px;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: center;

    @media (max-width: 800px) {
        background-color: #ff8f28;
        color: #ffffff;
        border-radius: 7%;
        height: 6rem;
        align-content: center;
        margin-inline: 24vw;
    }
}

.project-header {
    font-size: 1.5rem;
    color: #b94923;
    font-family: 'Aleo';

    @media (max-width: 800px) {
        padding: 1.5rem 0.5rem 0;
    }
}

.challenges-button,
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
    color: #ff8f28;
}

.challenges-button {
    padding-top: 0.5rem;
    color: #a49b83;
}

.challenges-hidden {
    display: none;
}

.no-challenges-hidden {
    display: none;
}

.challenges-shown {
    display: flex;
    flex-direction: column;
    width: 100%;
    font-family: 'Inter';

    @media (max-width: 800px) {
        padding-top: 1rem;
    }
}

.no-challenges-shown {
    display: flex;
    flex-direction: column;
    width: 100%;
    font-family: 'Inter';
    font-size: 0.75rem;
    font-weight: 600;
    padding-top: 1rem;

    @media (max-width: 800px) {
        text-align: center;
    }
}

.camera-style {
    width: 1.5rem;
}

.button-container {
    display: flex;
    flex-direction: column;

    @media (max-width: 800px) {
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
    }
}

.image-container {
    display: flex;
}

.team-url-style {
    text-decoration: none;
    color: inherit;
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
}

.arrow-right {
    transform: rotate(0deg);
}

.arrow-down {
    transform: rotate(90deg);
}
</style>