<template>
  <FitScreen mode="full" :height="1080" :width="1920">
    <div class="container">
      <div class="container-title">
        <span>AI行业生态全景图</span>
        <div class="container-search">
          <el-input
            v-model="inputValue"
            style="width: 200px,height: 36px,color: #333333"
            size="large"
            placeholder="搜索"
            :suffix-icon="Search"
            @change="handleSearch"
          />
        </div>
      </div>
      <div class="container-content">
        <div
          class="container-content-box"
          v-for="(item, index) in landscapeData"
          :key="index"
        >
          <ContentShow
            :showData="item"
            :listIndex="index"
            :searchData="searchData"
            @handleClick="handleClick"
            ref="contentShowRef"
          />
        </div>
      </div>
      <div class="footer">
        <div class="footer-left">
          <div class="down-pdf footer-box" @click="handleDownloadPdf">
            下载pdf
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
            >
              <path
                d="M10 2.5V12.5"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
              <path
                d="M5 8.75L10 12.5L14.375 8.75"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
              <path
                d="M3.75 17.5H16.25"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
            </svg>
          </div>
          <div class="feedback footer-box" @click="handleFeedback">
            我要反馈
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
            >
              <path
                d="M12 15L17 15"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
              <path
                d="M11.7143 3.82143C12.7202 2.81548 14.3512 2.81548 15.3571 3.82143V3.82143C16.3631 4.82738 16.3631 6.45834 15.3571 7.46429L7.8058 15.0156L3.82142 15.3571L4.16294 11.3728L11.7143 3.82143Z"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
              <path
                d="M8.9823 7.76794L12.018 10.8037"
                stroke="black"
                stroke-width="2"
                class="feedback-path"
              />
            </svg>
          </div>
        </div>
        <div class="footer-right">
          <LogoSvg />
          <div class="footer-logo-show" @click="handleClickGitHub">
            <img src="@/assets/public/git-hub-logo.png" />
          </div>
        </div>
      </div>
    </div>
    <teleport to="body">
      <div
        class="img-detail"
        v-if="isShowDialog"
        :style="{ top: dialogTop + 'px', left: dialogLeft + 'px' }"
      >
        <div class="img-detail-title">
          <img
            class="img-detail-title-img"
            :src="require(`@/assets/logos/${showDetailInfo?.logo}`)"
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="28"
            height="28"
            viewBox="0 0 28 28"
            fill="none"
            class="img-close"
            @click="handleClose"
          >
            <path
              d="M7.63635 7.63635L20.3636 20.3636"
              stroke="#666666"
              stroke-width="2"
            />
            <path
              d="M20.3636 7.63635L7.63635 20.3636"
              stroke="#666666"
              stroke-width="2"
            />
          </svg>
        </div>
        <div class="img-detail-title-text">
          {{ showDetailInfo?.name }}
        </div>
        <div class="img-detail-title-country">中国</div>
        <div class="img-detail-title-desc">
          {{ showDetailInfo?.description }}
        </div>
        <div class="img-detail-bottom-desc">
          <div class="img-detail-bottom-desc-one">
            创立于<span class="img-detail-bottom-desc-span">{{
              showDetailInfo?.founded_year
            }}</span>
          </div>
          <div class="img-detail-bottom-desc-one">
            文本展示<span class="img-detail-bottom-desc-span">xxx</span>
          </div>
          <div class="img-detail-bottom-desc-web" @click="pathStamp">
            <span class="web-text">网站</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
            >
              <path d="M15 9L14.9998 5H10.9998" stroke="black" />
              <path d="M15.091 5L11.2046 8.88642" stroke="black" />
              <path d="M8.33333 5H5V15H15V11.6667" stroke="black" />
            </svg>
          </div>
        </div>
      </div>
    </teleport>
  </FitScreen>
</template>
<script setup>
import { ref, onMounted, computed } from "vue";
import FitScreen from "@fit-screen/vue";
import jsyaml from "js-yaml";
import ContentShow from "../components/ContentShow.vue";
import LogoSvg from "../components/LogoSvg.vue";
import { exportToPDF } from "../utlis/pdfExport";
import { Search } from "@element-plus/icons-vue";

const landscapeData = ref([]);
const showDetailInfo = ref(null);
const contentShowRef = ref(null);
const isShowDialog = ref(false);
const inputValue = ref("");
const dialogTop = ref(0);
const dialogLeft = ref(0);
const searchData = ref([]);
onMounted(async () => {
  const response = await fetch("/static/data.yaml");
  const yamlText = await response.text();
  const parsedData = jsyaml.load(yamlText);
  landscapeData.value = parsedData?.landscape;
});
const handleSearch = () => {
  searchData.value = [];
  if (!inputValue.value) return searchData.value;
  landscapeData.value?.forEach((category) => {
    category.subcategories.forEach((item) => {
      item.items.forEach((it) => {
        if (it.name.includes(inputValue.value)) {
          searchData.value.push(it);
        }
      });
    });
  });
};
const handleTime = () => {
  return showDetailInfo.value?.description?.split(" ")?.[1]?.split("-")?.[0];
};
const handleClick = (props, it, clientY, clientX) => {
  isShowDialog.value = props;
  showDetailInfo.value = it;
  dialogTop.value = clientY;
  dialogLeft.value = clientX;
};
const handleClose = () => {
  isShowDialog.value = false;
};
const pathStamp = () => {
  window.location.href = showDetailInfo.value?.homepage_url;
};
const handleFeedback = () => {
  window.location.href = "https://github.com/openfusionx/FXView/issues";
};
const handleClickGitHub = () => {
  window.location.href = "https://github.com/openfusionx/FXView";
};
const handleDownloadPdf = () => {
  exportToPDF("app", "landscape.pdf");
};
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.firm-log {
  background: #e5fbf7;
  border-radius: 8px;
  padding: 12px;
}
.firm-list {
  min-height: 200px;
  border: 1px dotted #63be90;
  border-radius: 8px;
}
.container-title {
  width: 100%;
  height: 80px;
  flex-shrink: 0;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.05);
  font-family: "PingFang HK";
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 2px;
  padding-left: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.container-title span {
  background: linear-gradient(90deg, #e94fd5 0%, #6358f2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.container-search {
  position: absolute;
  top: 50%;
  right: 40px;
  margin-top: -18px;
  z-index: 22;
  -webkit-text-fill-color: none;
}
.container-content {
  width: 100%;
  padding: 20px;
  height: 86%;
  overflow-y: scroll;
}
.container-content-box {
  margin-bottom: 20px;
}
.img-detail {
  width: 340px;
  height: 340px;
  border-radius: 4px;
  border: 1px solid #c2ccd9;
  background: #fff;
  position: absolute;
  z-index: 99;
  padding: 20px;
}
.img-detail-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.img-detail-title-img {
  width: 120px;
  height: 40px;
  object-fit: cover;
}
.img-detail-title-text {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
}
.img-detail-title-country {
  color: #000;
  font-family: "PingFang HK";
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  opacity: 0.5;
}
.img-detail-title-desc {
  margin: 20px 0;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
}
.img-detail-bottom-desc {
  display: flex;
}
.img-detail-bottom-desc-one {
  color: rgba(0, 0, 0, 0.5);
  font-family: "PingFang HK";
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  margin-right: 20px;
}
.img-detail-bottom-desc-span {
  color: #000;
  margin-left: 8px;
}
.img-detail-bottom-desc-web {
  color: #000;
  font-family: Avenir;
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: auto;
  text-decoration-thickness: auto;
  text-underline-offset: auto;
  text-underline-position: from-font;
  display: flex;
}
.img-close:hover {
  cursor: pointer;
}
.img-detail-bottom-desc-web:hover {
  cursor: pointer;
  color: #d91b64;
  text-decoration-color: #d91b64;
}
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80px;
  width: 100%;
  padding: 0 20px;
  background: #f7f8fa;
  box-shadow: 4px 0px 8px 0px rgba(0, 0, 0, 0.05);
  position: fixed;
  left: 0;
  bottom: 0;
}
.footer-box {
  display: flex;
  padding: 6px 10px;
  justify-content: center;
  align-items: center;
  gap: 4px;
  border-radius: 4px;
  border: 1px solid #d5d5d5;
  /* border: 1px solid #df4a83; */
  background: #fff;
  width: 120px;
  height: 34px;
}
.footer-box:hover {
  cursor: pointer;
  border: 1px solid #df4a83;
  color: #d91b64;
}
.footer-box:hover :deep(.feedback-path) {
  stroke: #d91b64;
}
.footer-left {
  display: flex;
}
.footer-right {
  display: flex;
}
.footer-logo-show:hover {
  cursor: pointer;
}
.footer-logo-show img {
  width: 40px;
  height: 40px;
}
.down-pdf {
  margin-right: 20px;
}
:deep(.el-input__wrapper) {
  border-radius: 30px !important;
}
</style>
