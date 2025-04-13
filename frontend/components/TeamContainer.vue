<template>
  <div class="entire-container">
    <!-- If no teams pass the filter, show "No Submissions" -->
    <div class="no-submission-container" v-if="filteredCombinedValues.length === 0">
      <div class="no-submission">No Submissions</div>
    </div>

    <!-- If we have results, show the header row, then the content -->
    <div class="top-row" v-else>
      <div class="row-header-table"></div>
      <div class="row-header-project"></div>
    </div>

    <div class="content-row" :class="{ 'content-row-hidden': filteredCombinedValues.length === 0 }">
      <ProjectTeamInformation :filtered="state.filteredTeamNames" :challengeDetails="state.filteredChallengeNames"
        :projectType="state.projectType" :teamDetails="filteredCombinedValues" />
    </div>
    <div class="bottom-row"></div>
  </div>
</template>

<script>
import { inject, computed } from 'vue'
import ProjectTeamInformation from './ProjectTeamInformation.vue'

export default {
  name: 'TeamContainer',
  components: {
    ProjectTeamInformation
  },
  setup() {
    const state = inject('state')

    // We’ll filter state.teams here
    const filteredCombinedValues = computed(() => {
      if (!state.teams || state.teams.length === 0) return []

      return state.teams.filter((team) => {
        // 1) Project type check
        let typeCheck = true
        if (state.projectType === 'in-person') {
          typeCheck = team.in_person === true
        } else if (state.projectType === 'virtual') {
          typeCheck = team.in_person === false
        }

        // 2) Team name check
        // Only show this team if its name is in the filteredTeamNames
        const nameCheck = state.filteredTeamNames.includes(team.team_name)

        // 3) Challenge check
        // If no challenge was picked, or if the team has a challenge with that name
        let challengeCheck = true
        if (state.filteredChallengeNames) {
          // If user picked something, we only keep teams that have that challenge
          if (state.filteredChallengeNames !== '') {
            challengeCheck = team.challenges.some(
              (ch) => ch.challenge_name === state.filteredChallengeNames
            )
          }
        }

        return typeCheck && nameCheck && challengeCheck
      })
    })

    return { state, filteredCombinedValues }
  }
}
</script>

<style scoped lang="scss">
.entire-container {
  background-color: #f6ebcc;
  border-radius: 1.5rem;
  width: calc(20rem + 30vw);
  height: 30rem;

  @media (max-width: 800px) {
    width: calc(5rem + 65vw);
    height: 25rem;
    margin: 2rem auto;
  }

  .no-submission-container {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    .no-submission {
      color: #ffff;
      font-family: 'Aleo';
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 2rem;
      border-radius: 1.5rem;
      padding: 10rem;
      background-color: #ff8f28;
      margin: auto;
      padding: 5rem;
      height: calc(4rem + 17.5vh);
      width: calc(4rem + 30vw);

      @media (max-width: 800px) {
        font-size: 1.4em;
        height: calc(4rem + 9.5vh);
        width: calc(4rem + 20vw);
      }
    }
  }
}

.top-row {
  height: fit-content;
  display: flex;
  flex-direction: row;
  margin-inline: 1.25rem;
  padding: 1rem 0 0;
  padding-bottom: 0.5rem;
  border-bottom-color: #ff8f28;
  border-bottom-width: 0.069rem;
  border-bottom-style: solid;
}

.row-header-table {
  font-size: 1.5rem;
  width: 6rem;
  margin-right: 1.5rem;
  text-align: center;
  color: #295111;
  font-family: 'Aleo';
  min-width: 100px;

  @media screen and (max-width: 800px) {
    margin-right: 0;
  }
}

.row-header-project {
  font-size: 1.5rem;
  color: #295111;
  font-family: 'Aleo';

  @media screen and (max-width: 800px) {
    margin: auto;
  }
}

.row-header-table::before {
  content: 'Table';
}

.row-header-project::before {
  content: 'Project';
}

@media screen and (max-width: 800px) {
  .row-header-table {
    display: none;
  }

  .row-header-project::before {
    content: 'Project Information';
  }
}

.content-row {
  overflow-x: hidden;
  overflow-y: auto;
  max-height: 81%;
}

.content-row-hidden {
  display: none;
  height: 0;
  overflow: hidden;
}
</style>
