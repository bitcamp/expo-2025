<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="row-header-table">Table</div>
            <div class="row-header-project">Project</div>
        </div>
        <div class="content-row">
            <ProjectTeamInformation :filtered="state.filteredTeamNames" :challengeDetails="state.filteredChallengeNames"
                :projectType="state.projectType" :teamDetails="[['A0', 'Lakers', [['my', 'nutz', '69', 'times'], ['doze', 'nutz', '69', 'times'], ['your', 'nutz', '69', 'times'], ['everyone', 'nutz', '69', 'times']]],
            ['A1', 'Clippers', [['deez', 'nutz', '69', 'times'], ['doze', 'nutz', '69', 'times'], ['everyone', 'nutz', '69', 'times']]],
            ['virtual', 'Grizzlies', [['deez', 'nutz', '69', 'times'], ['everyone', 'nutz', '69', 'times']]],
            ['virtual', 'Cavs', [['everyone', 'nutz', '69', 'times']]]]" />

        </div>
        <div class="bottom-row">
        </div>
    </div>
</template>

<script>
import { inject, watchEffect } from "vue";
import ProjectTeamInformation from "./ProjectTeamInformation.vue";
import JudgingRow from "./JudgingRow.vue";


export default {
    name: 'TeamContainer',
    setup() {
        const state = inject('state');

        // watchEffect(() => {
        //     console.log(state.filteredTeamNames);
        // });

        // watchEffect(() => {
        //     if (state.filteredChallengeNames.length > 0) {
        //         console.log(state.filteredChallengeNames);
        //     }
        // });

        return { state };
    },
};
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');

.entire-container {
    background-color: #F6EBCC;
    border-radius: 1.5rem;
    width: calc(20rem + 25vw);
    height: 30rem;


    @media (max-width: 800px) {
        width: calc(5rem + 65vw);
        margin: 2rem auto;
    }
}

.top-row {
    height: fit-content;
    display: flex;
    flex-direction: row;
    margin-inline: 2rem;
    padding: 1.5rem 0 0;
    padding-bottom: 0.5rem;
    border-bottom-color: #FF8F28;
    border-bottom-width: 0.069rem;
    border-bottom-style: solid;
}

.row-header-table {
    font-size: 1.5rem;
    width: 6rem;
    margin-right: 2rem;
    text-align: center;
    color: #FF8F28;
    font-family: 'Aleo';
    min-width: 100px;

    @media screen and (max-width: 800px) {
      margin-right: 0rem;
    }
}

.row-header-project {
    font-size: 1.5rem;
    color: #FF8F28;
    font-family: 'Aleo';
}

.content-row {
    overflow-y: auto;
    max-height: 81%;
}
</style>