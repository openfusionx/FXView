<template>
  <div
    class="container-content-box-title"
    :style="{
      backgroundColor: currentTitleColor,
    }"
  >
    {{ showData?.name }}
  </div>
  <div
    class="container-content-box-show"
    :style="{
      backgroundColor: currentContentColor,
    }"
  >
    <div
      class="container-content-box-show-item"
      :class="{
        'container-content-box-show-item-last': index % 4 === 0 && index != 0,
      }"
      v-for="(item, index) in showData?.subcategories"
      :key="index"
    >
      <div class="container-content-box-show-item-title">
        {{ item.name }}
      </div>
      <div class="container-content-box-show-item-content">
        <div
          class="img-show"
          v-for="(it, ind) in item.items"
          :key="ind"
          @click="showCompanyInfo(it, $event)"
          :class="{
            'search-img':
              searchData?.findIndex((city) => city.name === it.name) !== -1
                ? true
                : false,
          }"
        >
          <img
            :src="require(`@/assets/logos/${it.logo}`)"
            class="img-item"
            :ref="(el) => setImgRef(el, index, ind)"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {
  ref,
  defineProps,
  watch,
  defineExpose,
  defineEmits,
  onMounted,
} from "vue";
const showDetailInfo = ref(false);
const currentTitleColor = ref(null);
const currentContentColor = ref(null);
const isShowDialog = ref(false);
const dialogTop = ref(0);
const dialogLeft = ref(0);
const imgRefs = ref([]);
const props = defineProps({
  showData: {
    type: Array,
    default: () => [],
  },
  listIndex: {
    type: Number,
    default: 0,
  },
  searchData: {
    type: Array,
    default: () => [],
  },
});
const bgTitleColor = ["#FE8FB9", "#A6BBE6", "#A6E6DB", "#AEA6E6"];
const bgContentColor = ["#FFF0F6", "#E2E8F3", "#EAF4F2", "#F6F5FF"];
const emit = defineEmits(["handleClick"]);
const showCompanyInfo = (it, event) => {
  isShowDialog.value = true;
  showDetailInfo.value = it;
  const viewportWidth = window.innerWidth;
  const target = event.currentTarget;
  const rect = target.getBoundingClientRect();
  // 获取页面滚动偏移量
  const scrollX = window.scrollX || window.pageXOffset;
  const scrollY = window.scrollY || window.pageYOffset;
  dialogTop.value =
    event.currentTarget.getBoundingClientRect().top +
    scrollY +
    target.offsetHeight -
    20;
  if (rect.left + 380 > viewportWidth) {
    // 右侧空间不足，改到左侧
    dialogLeft.value = rect.left + scrollX - 360 + target.offsetWidth;
  } else {
    dialogLeft.value = rect.left + scrollX + target.offsetWidth;
  }
  emit(
    "handleClick",
    isShowDialog.value,
    it,
    dialogTop.value,
    dialogLeft.value
  );
};
const setImgRef = (el, categoryIndex, ind) => {
  if (!imgRefs.value[categoryIndex]) {
    imgRefs.value[categoryIndex] = [];
  }
  if (el) {
    imgRefs.value[categoryIndex][ind] = el;
  }
};
const resizeImages = () => {
  imgRefs.value.forEach((it) => {
    if (!it) return;
    it.forEach((img) => {
      if (!img) return;
      const containerWidth = 60;
      const containerHeight = 20;
      const imgWidth = img.naturalWidth;
      const imgHeight = img.naturalHeight;
      if (containerWidth / imgWidth > containerHeight / imgHeight) {
        img.style.height = `${containerHeight}px`;
        img.style.width = (containerHeight / imgHeight) * imgWidth + "px";
      } else {
        img.style.width = `${containerWidth}px`;
        img.style.height = (containerWidth / imgWidth) * imgHeight + "px";
      }
    });
  });
};
onMounted(() => {
  resizeImages();
});
watch(
  () => props.listIndex,
  () => {
    currentTitleColor.value = bgTitleColor[props.listIndex];
    currentContentColor.value = bgContentColor[props.listIndex];
  },
  {
    immediate: true,
  }
);
defineExpose({
  showDetailInfo,
  isShowDialog,
});
</script>
<style scoped>
.container-content-box-title {
  width: 100%;
  height: 60px;
  flex-shrink: 0;
  padding-left: 40px;
  display: flex;
  align-items: center;
  color: #000;
  text-align: center;
  font-family: "PingFang HK";
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 2px;
}
.container-content-box-show {
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-wrap: wrap;
}
.container-content-box-show-item {
  margin-right: 6px;
  margin-top: 10px;
  width: 362px;
  box-sizing: border-box;
}
.container-content-box-show-item-last {
  margin-right: 0px;
}
.container-content-box-show-item-title {
  height: 40px;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: #fff;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container-content-box-show-item-content {
  padding: 20px;
  background: #fff;
  min-height: 164px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 48px);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
}
.img-show {
  width: 80px;
  height: 48px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.img-show:hover {
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fff;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.05);
}
.search-img {
  border-radius: 4px;
  border: 1px solid #d91b64;
  background: #fff;
  box-shadow: 0px 4px 8px 0px #d91b64;
}
</style>
