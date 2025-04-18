<template>
  <div class="entire-container-filter">
    <div class="top-row">
      <div class="filter-header">Filter</div>
    </div>
    <div class="filters">
      <!-- Filter by Team Name -->
      <div class="filter-item">
        <div class="filter-title">Name</div>
        <input class="search-box" type="text" placeholder="Search..." @input="searchTeamNames($event)" />
      </div>
      <!-- Filter by Challenge -->
      <div class="filter-item">
        <div class="filter-title">Challenges</div>
        <select name="challenge" class="select-box" id="challenge" @change="searchChallengeNames($event)">
          <option value="none">All Challenges</option>
          <option v-for="(name, idx) in challengeNames" :key="idx" :value="name">
            {{ name }}
          </option>
        </select>
      </div>
      <!-- Filter by Project Type -->
      <div class="filter-item">
        <div class="filter-title">Project Type</div>
        <select name="project-type" class="select-box" id="project-type" @change="searchProjectType($event)">
          <option value="all">All Projects</option>
          <option value="in-person">In-Person Projects</option>
          <option value="virtual">Virtual Projects</option>
        </select>
      </div>
    </div>
    <div class="bottom-row"></div>
  </div>
</template>

<script>
import { inject, watch, onMounted } from 'vue'

export default {
  name: 'FilterComponent',
  props: {
    challengeNames: {
      type: Array,
      required: true
    },
    teamNames: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const state = inject('state')

    // Whenever the full list of team names changes, reset the filtered list
    watch(
      () => props.teamNames,
      (newVal) => {
        state.filteredTeamNames = newVal
      },
      { immediate: true }
    )

    onMounted(() => {
      // Reset these on load
      state.filteredChallengeNames = ''
      state.projectType = 'all'
    })

    const searchTeamNames = (event) => {
      const searchTerm = event.target.value.toLowerCase()
      if (!searchTerm) {
        // no search
        state.filteredTeamNames = props.teamNames
      } else {
        state.filteredTeamNames = props.teamNames.filter((name) =>
          name.toLowerCase().includes(searchTerm)
        )
      }
    }

    const searchChallengeNames = (event) => {
      const selected = event.target.value
      if (selected === 'none') {
        state.filteredChallengeNames = ''
      } else {
        // just store the chosen challenge name
        state.filteredChallengeNames = selected
      }
    }

    const searchProjectType = (event) => {
      state.projectType = event.target.value
    }

    return {
      searchTeamNames,
      searchChallengeNames,
      searchProjectType
    }
  }
}
</script>

<style scoped lang="scss">
.entire-container-filter {
  background-color: #f6ebcc;
  width: calc(5rem + 10vw);
  min-width: 10rem;
  height: 25.1rem;
  border-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1.5rem 3.3rem;
  margin-right: 1rem;
  overflow-x: hidden;

  @media (max-width: 800px) {
    width: calc(2rem + 65vw);
    margin: 0 2rem;
  }
}

.filter-header {
  font-family: 'Aleo';
  color: #295111;
  font-weight: 400;
  font-size: 1.5rem;
}

.top-row {
  margin-bottom: 1.5rem;
}

.search-box {
  width: 100%;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  border: 2px solid #ff8e3f;
  background-color: #fff9ed;
  font-family: 'Inter';
  margin-bottom: 1rem;
  outline: none;
  box-sizing: border-box;
}

.select-box {
  width: 100%;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  background-color: #b94923;
  border: 2px solid #b94923;
  font-family: 'Inter';
  margin-bottom: 1rem;
  color: white;
  border-right: 0.75rem solid transparent;
  cursor: pointer;
}

.filter-title {
  margin-bottom: 0.5rem;
  margin-left: 1rem;
  font-family: 'Inter';
  font-weight: 300;
}

.filters {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: flex-start;
}

.filter-item {
  margin-bottom: 1rem;
  width: 100%;
}

@media (max-width: 800px) {
  .search-box {
    width: calc(54% + 32vw);
  }

  .filter-item {
    margin-bottom: 0;
  }

  .filter-title {
    display: none;
    margin-bottom: 0;
  }

  .entire-container-filter {
    height: auto;
    padding-bottom: 1rem;
  }
}
</style>
