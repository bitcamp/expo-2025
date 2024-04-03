<template>
  <div class="entire-container-filter">
    <div class="top-row">
      <div class="filter-header">Filter</div>
    </div>
    <div class="filters">
      <div class="filter-item">
        <div class="filter-title">Name</div>
        <input class="search-box" type="text" placeholder="Search for Project" @input="searchTeamNames($event)" />
      </div>
      <div class="filter-item">
        <div class="filter-title">Challenges</div>
        <select name="challenge" class="select-box" id="challenge">
          <option value="none">None</option>
          <option v-for="(name, index) in challengeName" :key="index" :value="index">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <div class="filter-title">Project Type</div>
        <select name="project-type" class="select-box" id="project-type">
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
import { inject } from 'vue';

export default {
  name: 'FilterComponent',
  props: {
    challengeName: {
      type: Array,
      required: true,
    },
    teamNames: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const state = inject('state');

    onMounted(() => {
      state.filteredTeamNames = props.teamNames;
    });

    const searchTeamNames = (event) => {
      const searchTerm = event.target.value.toLowerCase();
      if (searchTerm === "") {
        state.filteredTeamNames = props.teamNames;
      }
      else {
        state.filteredTeamNames = props.teamNames.filter(name =>
          name.toLowerCase().includes(searchTerm)
        );
      }
    };
    console.log("filtered" + state.filteredTeamNames);
    console.log("search" + searchTeamNames);
    return { searchTeamNames };
  },
};
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

.entire-container-filter {
  background-color: #F6EBCC;
  width: calc(5rem + 10vw);
  min-width: 10rem;
  height: 25.1rem;
  border-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1.5rem 3.3rem;
  margin-right: 1rem;

  @media (max-width: 800px) {
    width: calc(2rem + 65vw);
    margin: 0 2rem;
  }
}

.filter-header {
  font-family: 'Aleo';
  color: #FA9747;
  font-weight: 400;
  font-size: 1.5rem;
}

.top-row {
  margin-bottom: 1.5rem;
}

.search-box {
  width: 80%;
  padding: 0.5rem;
  border-radius: 2rem;
  border: 2px solid #FF8E3F;
  background-color: #FFF9ED;
  font-family: 'Inter';
  margin-bottom: 1rem;
  padding-inline: 1rem;
}

.select-box {
  width: 100%;
  padding: 0.5rem;
  border-radius: 2rem;
  border: 0.1rem solid #FF8E3F;
  background-color: #FF8E3F;
  font-family: 'Inter';
  margin-bottom: 1rem;
  color: white;
  padding-inline: 1rem;
  border-right: 0.75rem solid transparent
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
    width: calc(45% + 32vw);
  }
}
</style>
