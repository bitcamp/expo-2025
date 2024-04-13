<template>
  <div class="entry">
    <div class="project-description">
      <div class="category-name">{{ categoryName }}</div>
      <!-- <div class="middle-char"></div> -->
    </div>
    <div class="judging-description" v-if="companyName !== 'Major League Hacking'">
      <div>{{ companyName }}</div>
      <div class="judging-description-inner">
        <div>{{ judgeName }}</div>
        <div class="middle-char">-</div>
        <div>{{ newTime }}</div>
      </div>
    </div>
    <div class="judging-description-mlh" v-if="companyName === 'Major League Hacking'">
      <div>{{ companyName }}</div>
      <div>Consult MLH</div>
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
  setup(props) {
    const totalBlocks = ref(0);
    const newTime = ref(0);

    const fetchData = async () => {
      const response = await fetch("/expo_algorithm_results.json");
      const data = await response.json();
      totalBlocks.value = Number(props.timing) * Math.floor(180 / data.total_times);
      const baseTime = "10:15";
      newTime.value = addMinutesToTime(baseTime, totalBlocks.value);
      const [hours, minutes] = newTime.value.split(":").map(Number);
      if (Number(hours) < 12) {
        newTime.value = newTime.value + " AM";
      }
      else {
        newTime.value = newTime.value + " PM";
      }
    };

    const addMinutesToTime = (baseTime, minutesToAdd) => {
      const [hours, minutes] = baseTime.split(":").map(Number);
      const totalMinutes = hours * 60 + minutes + minutesToAdd;
      const resultHours = Math.floor(totalMinutes / 60);
      const resultMinutes = totalMinutes % 60;
      return `${resultHours}:${resultMinutes.toString().padStart(2, '0')}`;
    };

    onMounted(() => {
      fetchData();
    });

    return { totalBlocks, newTime };

  },
};
</script>

<style scoped lang="scss">
.entry {
  background-color: #f8eccc;
  width: 96%;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

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
  }

  .judging-description-inner {
    display: flex;
    flex-direction: row;
  }

  .judging-description-mlh {
    display: flex;
    font-size: 0.75rem;
    font-weight: 400;
    justify-content: space-between;
  }
}

.middle-char {
  margin-inline: 0.5rem;
}
</style>
