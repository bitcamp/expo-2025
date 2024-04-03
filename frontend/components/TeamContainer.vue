<template>
    <div class="entire-container">
        <div class="top-row">
            <div class="row-header-table">Table</div>
            <div class="row-header-project">Project</div>
        </div>
        <div class="content-row">
            <ProjectTeamInformation :filtered="state.filteredTeamNames"
                :challengeDetails="['deez','doze','your','everyone']"
                :teamDetails="[['Table', 'Lakers', [[ 'nutz', '69', 'times'], ['doze', 'nutz', '69', 'times'], ['your', 'nutz', '69', 'times'], ['everyone', 'nutz', '69', 'times']]],
            ['A1', 'Clippers', [['deez', 'nutz', '69', 'times'], ['doze', 'nutz', '69', 'times'], ['your', 'nutz', '69', 'times'], ['everyone', 'nutz', '69', 'times']]]]"/>
                
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

        watchEffect(() => {
            console.log(state.filteredTeamNames);
        });

        watchEffect(() => {
            if (state.filteredChallengeNames.length > 0) {
                console.log(state.filteredChallengeNames);
            }
        });

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


    @media (max-width: 850px) {
        width: calc(15rem + 55vw);
        margin-top: 2rem;
    }
}

.row-header-project,
.row-header-table {
    font-family: 'Aleo';
}

.top-row {
    height: fit-content;
    display: flex;
    flex-direction: row;
    margin-inline: 2rem;
    padding: 1rem;
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
}

.row-header-project {
    font-size: 1.5rem;
    color: #FF8F28;
}
</style>