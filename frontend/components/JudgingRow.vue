<template>
  <div class="entry">
    <div class="project-description">
      <div class="category-name">{{ categoryName }}</div>
    </div>

    <!-- If this challenge is MLH, show "Consult MLH" -->
    <div class="judging-description-mlh" v-if="isMLH">
      <div>Major League Hacking</div>
      <div>Consult MLH</div>
    </div>

    <!-- Otherwise show company + judge + startTime -->
    <div class="judging-description" v-else>
      <div>{{ companyName }}</div>
      <div class="judging-description-inner">
        <div>{{ judgeName }}</div>
        <div class="middle-char">-</div>
        <div>{{ displayTime }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'JudgingRow',
  props: {
    categoryName: {
      type: String,
      required: true
    },
    companyName: {
      type: String,
      required: true
    },
    judgeName: {
      type: String,
      required: true
    },
    startTime: {
      type: String,
      required: true
    },
    isMLH: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    // Optionally parse the 2024-04-21 11:00:00-04:00 string to a friendlier time
    const displayTime = computed(() => {
      if (!props.startTime) return ''
      // If there's no time (maybe for an MLH challenge?), might be empty
      // Otherwise, parse or format it
      try {
        const d = new Date(props.startTime)
        // e.g. "11:00 AM"
        const hours = d.getHours() % 12 || 12
        const minutes = d.getMinutes().toString().padStart(2, '0')
        const ampm = d.getHours() >= 12 ? 'PM' : 'AM'
        return `${hours}:${minutes} ${ampm}`
      } catch (err) {
        // fallback
        return props.startTime
      }
    })

    return {
      displayTime
    }
  }
}
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
      content: '|';
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
