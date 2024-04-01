<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="row-header-table">Table</div>
            <div class="row-header-project">Project</div>
        </div>
        <div class="content-row">
            <ProjectTitleComponent :teamDetails="[['A1', 'Team Name']]" />
        </div>
        <div class="bottom-row">
        </div>
    </div>
</template>

<script setup lang="ts">
import ProjectTitleComponent from "./ProjectTitleComponent.vue";
import JudgingRow from "./JudgingRow.vue";

</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');
.entire-container {
    background-color: #F6EBCC;
    border-radius: 1.5rem;
    width: calc(20rem + 25vw);
    height: 30rem;
}

.row-header-project, .row-header-table {
  font-family: 'Aleo';
}

.top-row {
    height: fit-content;
    display: flex;
    flex-direction: row;
    padding: 1.5rem;
    border-bottom-color: #FF8F28;
    border-bottom-width: 0.1rem;
    border-bottom-style: solid;
}

.row-header-table {
    font-size: 1.5rem;
    width: 6rem;
    text-align: center;
    color: #FF8F28;
}

.row-header-project {
    font-size: 1.5rem;
    color: #FF8F28;
}
</style>