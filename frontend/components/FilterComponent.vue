<template>
  <div class="entire-container">
    <div class="top-row">
      <div class="UI-header">Filter</div>
    </div>
    <div class="search">
      <div class="search-title">Name</div>
      <input class="search-box" type="text" placeholder="Search..." />
    </div>
    <div class="filters">
      <div class="filter-item">
        <label for="challenge">Challenge Name</label>
        <select name="challenge" id="challenge">
          <option value="none">None</option>
          <option value="1">Challenge 1</option>
          <option value="2">Challenge 2</option>
          <option value="3">Challenge 3</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="project-type">Project Type</label>
        <select name="project-type" id="project-type">
          <option value="all">All Projects</option>
          <option value="in-person">In-Person Projects</option>
          <option value="virtual">Virtual Projects</option>
        </select>
      </div>
    </div>
    <div class="bottom-row"></div>
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

.entire-container {
  background-color: #F6EBCC;
  width: 17rem;
  height: 30rem;
  border-radius: 2rem;
  display: flex;
  flex-direction: column;
  padding: 2rem; 
}

.UI-header {
  font-family: 'Aleo';
  color: #FA9747;
  font-weight: 400;
  font-size: 2.5rem;
}

.top-row,
.bottom-row {
  height: 5rem;
  display: flex;
  flex-direction: row;
}

.search-box {
  width: 90%;
  padding: 0.5rem;
  border-radius: 15px;
  border: 2px solid #FF8E3F;
  background-color: #FFF9ED;
  font-family: 'Inter';
  margin-bottom: 2rem;
}

.search-title {
  margin-bottom: 0.5rem; 
}

.filters {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.filter-item {
  margin-bottom: 1rem;
}

select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 15px;
  border: 0.1rem solid #ccc; 
}
</style>
