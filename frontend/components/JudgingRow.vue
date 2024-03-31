<template>
    <div class="entry">
        <div class="project-description">
            <div class="category-name">{{ categoryName }}</div>
            <div class="middle-char">|</div>
            <div>{{ companyName }}</div>
        </div>
        <div class="judging-description">
            <div>{{ judgeName }}</div>
            <div class="middle-char">-</div>
            <div>{{ timing }}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'JudgingRow',
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

<style scoped lang="scss">
.entry {
    display: flex;
    align-items: center;
    background-color: #f8eccc;
    justify-content: space-between;
    width: 100%;

    .project-description {
        display: flex;

        .category-name {
            font-weight: bold;
        }
    }

    .judging-description {
        display: flex;

    }
}

.middle-char {
    margin-inline: 0.5rem;
}
</style>