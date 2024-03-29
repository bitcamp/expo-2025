<template>
    <div class="entry">
        <div class = "project-description">
            <div class = "category-name">{{ categoryName }}</div>
            <div>|</div>
            <div>{{ companyName}}</div>      
        </div>
        <div class = "judging-description">
            <div>{{ judgeName }}</div>
            <div>-</div>
            <div>{{ timing }}</div>
        </div>
    </div>  
</template>

<script>
export default {
    name: 'SaiBad',
    props: {
    categoryName: {
        type: String,
        required: true,
    },
    companyName: {
        type: String,
        required: true,
    },
    judgeName: {
        type: String,
        required: true,
    },
    timing: {
        type: String,
        required: true,
    },
    },
};
</script>

<style lang="scss">
.entry {
    display: flex;
    align-items: center;
    background-color: #f8eccc;
    justify-content: space-between;

    .project-description{
        display: flex;

        div {
            font-family: Inter;
            margin: 5px 0;
            padding: 0 10%;
        }

        .category-name{
            font-weight: bold;
        }
    }

    .judging-description{
        display: flex;

    }
}





</style>