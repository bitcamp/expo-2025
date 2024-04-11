<template>
  <div class="entry">
    <div class="project-description">
      <div class="category-name">{{ categoryName }}</div>
    </div>
    <div class="judging-description">
      <div>{{ companyName }}</div>
      <div class="judging-description">
        <div>{{ judgeName }}</div>
        <div class="middle-char">-</div>
        <div>{{ timing }}</div>
      </div>
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
  background-color: #f8eccc;
  width: 96%;
  padding-top: 1rem;

  .project-description {
    display: flex;
    font-size: 0.75rem;
    font-weight: 400;
    padding-right: 2rem;

    @media (max-width: 800px) {
      display: inline-block !important;
    }

    .category-name {
      font-weight: 600;
    }

    .middle-char::before {
      content: "|";
    }

    @media screen and (max-width: 800px) {
      .middle-char {
        display: none;
      }
    }
  }

  .judging-description {
    display: flex;
    justify-content: space-between;
    flex-wrap: nowrap;
    font-size: 0.75rem;
    font-weight: 400;
    text-align: center;
  }
}

.middle-char {
  margin-inline: 0.5rem;
}
</style>
