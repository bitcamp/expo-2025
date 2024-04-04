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
  justify-content: space-between;
  flex-wrap: wrap; 
  background-color: #f8eccc;
  width: 95%;
  padding-top: 0.6rem;

  .project-description {
    display: flex;
    font-size: 14px;
    font-weight: 400;
    padding-right: 2rem;

    .category-name {
      font-weight: 600;
    }
  }

  .judging-description {
    display: flex;
    font-size: 14px;
    font-weight: 400;
  }
}

.middle-char {
  margin-inline: 0.5rem;
}
</style>
