<template>
  <div class="entire-container-filter">
    <div class="top-row">
      <div class="UI-header">Filter</div>
    </div>
    <div class="filters">
      <div class="filter-item">
        <div class="filter-title">Name</div>
        <input class="search-box" type="text" placeholder="Search for the Project Name" />
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
export default {
  name: 'FilterComponent',
  props: {
    challengeName: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    console.log(this.challengeName);
  },
};
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

.entire-container-filter {
  background-color: #F6EBCC;
  width: 15rem;
  height: 30rem;
  border-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  margin-inline: 2rem;
}

.UI-header {
  font-family: 'Aleo';
  color: #FA9747;
  font-weight: 400;
  font-size: 1.5rem;
}

.top-row {
  margin-bottom: 1.5rem;
}

.search-box {
  width: 90%;
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
}

.filter-title {
  margin-bottom: 0.5rem;
  margin-left: 1.5rem;
}

.filters {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.filter-item {
  margin-bottom: 1rem;
  width: 100%;
}
</style>
