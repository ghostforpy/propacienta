<template>
  <div>
    <!-- <v-btn
      small
      class="mt-2 white-content"
      style="width: 100%"
      color="cyan lighten-2"
      rounded
      @click="callHandler"
    >
      Позвонить
    </v-btn> -->
    <v-snackbar
      v-model="snackbarIncomeCall"
      centered
      vertical
      timeout="-1"
      content-class="snackbar-content-class"
    >
      <span>{{ snackbarIncomeCallText }}</span>
      <div class="snackbar-content-btn-class">
        <v-btn fab color="green" @click="accept_income_call">
          <v-icon color="white">mdi-phone</v-icon>
        </v-btn>
        <v-btn fab color="red" @click="reject_income_call">
          <v-icon color="white" class="rotate-dial">mdi-phone</v-icon>
        </v-btn>
      </div>
    </v-snackbar>

    <v-card
      v-bind:style="cardPosition"
      @mousedown="cardMouseDownHandle"
      @mouseup="cardMouseUpHandle"
      @mouseleave="cardMouseUpHandle"
      :loading="dialInProgress"
      :height="localVideo ? 380 : 220"
      width="150"
      color="grey"
      class="dial-card-posiotion"
      v-show="dialCardShow"
      ref="dialCard"
      id="dialCard"
    >
      <v-img
        v-if="!dialWithRemoteVideo"
        class="grey-background"
        height="150"
        contain
        :src="avatarSrc"
      ></v-img>
      <!-- <video
        v-if="dialWithRemoteVideo"
        ref="refRemoteVideo"
        width="150"
        height="150"
        autoplay
      ></video> -->
      <video
        v-if="localVideo"
        ref="refLocalVideo"
        width="150"
        height="150"
        autoplay
        muted
      ></video>
      <br />
      <v-card-text class="text-center">
        <v-btn fab small color="red lighten-1" @click="discardCallHandler"
          ><v-icon color="white" class="rotate-dial">mdi-phone</v-icon></v-btn
        >
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
import { BASE_URL } from "@/api/HTTP";

export default {
  name: "WebDial",
  props: {
    // opponentId: Number,
    // opponentType: String,
    //   lastName: String,
    //   patronymic: String,
    //   birthday: String,
  },
  data: function () {
    return {
      cardPosition: { left: "10px", top: "70px" },
      cardMove: false,
      opponentId: null,
      opponentType: null,
      dialCardShow: true,
      dialInProgress: true,
      dialWithRemoteVideo: false,
      localVideo: true,
      signalWebsocket: null,
      mediaStreamLocal: null,
      mediaStreamRemote: null,
      pc: null,
      dialUUID: null,
      snackbarIncomeCall: false,
      snackbarIncomeCallText: "Вызов",
      credentials: null,
      shiftPosCard: null,
    };
  },
  mounted: function () {
    var vuel = this;
    this.$eventBus.$on(
      "initDial",
      ({ opponentId: opponentId, opponentType: opponentType }) => {
        vuel.opponentId = opponentId;
        vuel.opponentType = opponentType;
        // vuel.initCall();
        vuel.initRTCPeerconnection();
        vuel.signalWebsocket.send(
          JSON.stringify({
            event: "init_call",
            opponentId: vuel.opponentId,
            opponentType: vuel.opponentType,
          })
        );
      }
    );
    var dialElem = document.getElementById("dialCard");

    dialElem.addEventListener("touchstart", this.cardMouseDownHandle);
    dialElem.addEventListener("touchend", this.cardMouseUpHandle);

    this.signalWebsocket = new WebSocket("wss://" + BASE_URL + "/ws/webdials/");
    this.signalWebsocket.onclose = function () {
      vuel.localMediaStreamOff();
      // window.alert("Websocket has closed");
    };
    // this.signalWebsocket.onerror = function (evt) {
    this.signalWebsocket.onerror = function () {
      vuel.localMediaStreamOff();
      // console.log("ERROR: " + evt.data);
    };

    this.signalWebsocket.onmessage = function (evt) {
      // console.log(evt);
      let msg = JSON.parse(evt.data);
      if (!msg) {
        return console.log("failed to parse msg");
      }
      if (msg.event == "offer") {
        let offer = JSON.parse(msg.data);
        if (!offer) {
          return console.log("failed to parse offer");
        }
        vuel.dialUUID = msg.dial_uuid;
        navigator.mediaDevices
          .getUserMedia({ video: true, audio: true })
          .then((stream) => {
            vuel.mediaStreamLocal = stream;

            vuel.$refs.refLocalVideo.srcObject = stream;
            stream
              .getTracks()
              .forEach((track) => vuel.pc.addTrack(track, stream));
            vuel.pc
              .setRemoteDescription(offer)
              .then(() => console.log("offer is set"))
              .catch(() => console.log("offer no good"));
            vuel.pc.createAnswer().then((answer) => {
              vuel.pc.setLocalDescription(answer);
              console.log(offer, answer);
              vuel.signalWebsocket.send(
                JSON.stringify({
                  event: "answer",
                  dial_uuid: msg.dial_uuid,
                  data: JSON.stringify(answer),
                })
              );
            });
          });

        // return;
      } else if (msg.event == "candidate") {
        let candidate = JSON.parse(msg.data);
        if (!candidate) {
          return console.log("failed to parse candidate");
        }
        // console.log("income candidate", candidate);
        // setInterval(() => {
        vuel.pc
          .addIceCandidate(new RTCIceCandidate(candidate))
          .then(() => console.log("good candidate"))
          .catch(() => console.log("error candidate"));
        // }, 100); // какая-то хрень
      } else if (msg.event == "answer") {
        let answer = JSON.parse(msg.data);
        vuel.dialUUID = msg.dial_uuid;

        if (!answer) {
          return console.log("failed to parse answer");
        }
        vuel.pc.setRemoteDescription(answer);
      } else if (msg.event == "init_call") {
        // добавить кнопку приема вызова, пока прием по умолчанию
        // if (accept) {
        // vuel.initRTCPeerconnection();
        vuel.dialUUID = msg.dial_uuid;
        vuel.snackbarIncomeCallText = msg.init_call_username;
        // vuel.signalWebsocket.send(
        //   JSON.stringify({
        //     event: "accept_init_call",
        //     dial_uuid: msg.dial_uuid,
        //   })
        // );
        vuel.snackbarIncomeCall = true;
        // } else {
        //         vuel.signalWebsocket.send(
        // JSON.stringify({
        //   event: "reject_init_call",
        //   dial_uuid: msg.dial_uuid,
        // }
        // )
        // );
      } else if (msg.event == "accept_init_call") {
        vuel.dialUUID = msg.dial_uuid;
        // init call
        vuel.initCall();
      } else if (msg.event == "reject_init_call") {
        vuel.dialUUID = null;
        vuel.localMediaStreamOff();
        vuel.endCall();
        // reject call
      } else if (msg.event == "end_call") {
        vuel.dialUUID = null;
        vuel.localMediaStreamOff();
        vuel.endCall();
        // end call
      } else if (msg.event == "dial_in_progres") {
        vuel.dialUUID = msg.dial_uuid;
        // dial in progres
      } else if (msg.event == "get_coturn_credentials") {
        vuel.credentials = msg.credentials;
      }
    };
    // this.WebSocket.onopen = this.get_coturn_credentials();

    // };
  },
  computed: {
    avatarSrc: function () {
      return require("@/assets/doctor_dial_avatar.jpeg");
    },
  },
  methods: {
    cardMouseDownHandle(event) {
      this.cardMove = true;
      // console.log(
      //   "handle cardMouseDownHandle",
      //   event.clientY,
      //   event.target.getBoundingClientRect().top
      // );
      var elem = document.getElementById("dialCard");
      this.shiftPosCard = {
        x: event.clientX - elem.getBoundingClientRect().left,
        y: event.clientY - elem.getBoundingClientRect().top,
      };
      document.addEventListener("mousemove", this.moveCard);
    },
    cardMouseUpHandle() {
      this.cardMove = false;
      document.removeEventListener("mousemove", this.moveCard);
      console.log("cardMouseUpHandle handle");
    },
    cardDBClickHandle() {
      console.log("cardDBClickHandle handle");
    },
    moveCard(event) {
      if (this.cardMove) {
        console.log(
          event.clientX,
          event.x,
          event.pageX,
          this.shiftPosCard.x,
          event.x - this.shiftPosCard.x + "px"
        );
        // const oldPositionLeft = parseInt(this.cardPosition.left.slice(0, -2));
        // const oldPositionTop = parseInt(this.cardPosition.top.slice(0, -2));
        var elem = document.getElementById("dialCard");
        const width = elem.getBoundingClientRect().width;
        const height = elem.getBoundingClientRect().height;

        if (
          !(
            event.x - this.shiftPosCard.x < 10 ||
            event.x - this.shiftPosCard.x >
              document.documentElement.clientWidth - 10 - width
          )
        ) {
          this.cardPosition.left =
            (event.x - this.shiftPosCard.x).toString() + "px";
        }
        // if (
        //   event.x - this.shiftPosCard.x >
        //   document.documentElement.clientWidth - 10 - width
        // ) {
        //   return;
        // }
        if (
          !(
            event.y - this.shiftPosCard.y < 70 ||
            event.y - this.shiftPosCard.y >
              document.documentElement.clientHeight - 10 - height
          )
        ) {
          this.cardPosition.top =
            (event.y - this.shiftPosCard.y).toString() + "px";
        }
        // if (
        //   event.y - this.shiftPosCard.y >
        //   document.documentElement.clientHeight - 10 - height
        // ) {
        //   return;
        // }
        // event.x - this.shiftPosCard.x + "px";
        // this.cardPosition.left =
        //   (event.x - this.shiftPosCard.x).toString() + "px";
        // (oldPositionLeft + event.movementX).toString() + "px";
        // this.cardPosition.top =
        //   (event.y - this.shiftPosCard.y).toString() + "px";

        // (oldPositionTop + event.movementY).toString() + "px";
      }
    },
    get_coturn_credentials() {
      this.signalWebsocket.send(
        JSON.stringify({
          event: "get_coturn_credentials",
        })
      );
    },
    handle_income_call() {
      this.snackbarIncomeCall = true;
    },
    accept_income_call() {
      this.initRTCPeerconnection();
      this.signalWebsocket.send(
        JSON.stringify({
          event: "accept_init_call",
          dial_uuid: this.dialUUID,
        })
      );
      this.snackbarIncomeCall = false;
    },
    reject_income_call() {
      this.signalWebsocket.send(
        JSON.stringify({
          event: "reject_init_call",
          dial_uuid: this.dialUUID,
        })
      );
      this.snackbarIncomeCall = false;
    },
    endCall() {
      if (this.pc != undefined) {
        this.pc.close();
        this.pc = null;
      }
      this.dialUUID = null;
      this.dialCardShow = false;
      document.getElementById("remoteVideo").remove();
    },
    localMediaStreamOff() {
      this.mediaStreamLocal.getTracks().forEach(function (track) {
        track.stop();
      });
    },
    initRTCPeerconnection() {
      var vuel = this;
      this.pc = new RTCPeerConnection({
        iceTransportPolicy: "relay",
        iceServers: [
          { urls: `stun:${BASE_URL}` },
          {
            urls: `turn:${BASE_URL}:3478`,
            username: this.credentials.username,
            credential: this.credentials.password,
          },
          // {
          //   urls: "stun:openrelay.metered.ca:80",
          // },
          // {
          //   urls: "turn:openrelay.metered.ca:80",
          //   username: "openrelayproject",
          //   credential: "openrelayproject",
          // },
          // {
          //   urls: "turn:openrelay.metered.ca:443",
          //   username: "openrelayproject",
          //   credential: "openrelayproject",
          // },
          // {
          //   urls: "turn:openrelay.metered.ca:443?transport=tcp",
          //   username: "openrelayproject",
          //   credential: "openrelayproject",
          // },
        ],
      });

      this.pc.ontrack = function (event) {
        if (event.track.kind === "audio") {
          return;
        }
        vuel.dialCardShow = true;
        vuel.dialWithRemoteVideo = true;
        let el = document.createElement(event.track.kind);
        el.srcObject = event.streams[0];
        el.autoplay = true;
        el.width = 150;
        el.height = 150;
        el.id = "remoteVideo";
        vuel.$refs.refLocalVideo.before(el);
        event.track.onmute = function () {
          var playPromise = el.play();
          if (playPromise !== undefined) {
            playPromise
              .then(() => {
                // Automatic playback started!
                // Show playing UI.
              })
              .catch(() => {
                // Auto-play was prevented
                // Show paused UI.
              });
          }
        };
      };
      this.pc.onconnectionstatechange = (ev) => {
        if (ev.target.connectionState === "connected") {
          // console.log(ev);
          this.dialWithRemoteVideo = true;
        }
      };
      this.pc.onicecandidate = (e) => {
        // window.alert("i send candidate");
        if (!e.candidate) {
          return;
        }

        console.log("on ice candidate", e.candidate);
        vuel.signalWebsocket.send(
          JSON.stringify({
            event: "candidate",
            dial_uuid: vuel.dialUUID,
            // opponentId: vuel.opponentId,
            // opponentType: vuel.opponentType,
            data: JSON.stringify(e.candidate),
          })
        );
      };
    },

    initCall() {
      var vuel = this;
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: true })
        .then((stream) => {
          vuel.mediaStreamLocal = stream;
          vuel.$refs.refLocalVideo.srcObject = stream;
          stream
            .getTracks()
            .forEach((track) => vuel.pc.addTrack(track, stream));
          // await this.getUserMedia();
          vuel.pc.createOffer().then((offer) => {
            vuel.pc.setLocalDescription(offer);
            vuel.signalWebsocket.send(
              JSON.stringify({
                event: "offer",
                dial_uuid: vuel.dialUUID,
                // opponentId: vuel.opponentId,
                // opponentType: vuel.opponentType,
                // initiator: {opponentId:}
                data: JSON.stringify(offer),
              })
            );
          });
          // .then(() => {
          //   console.log("create offer");
          //   vuel.signalWebsocket.send(
          //     JSON.stringify({
          //       event: "init_call",
          //       opponentId: vuel.opponentId,
          //       opponentType: vuel.opponentType,
          //       type: "video-offer",
          //       sdp: vuel.pc.localDescription,
          //     })
          //   );
          // });

          // ws.onclose = function (evt) {
        })
        .catch(window.alert);
    },
    callHandler() {
      this.dialCardShow = true;
      this.initCall();
    },
    discardCallHandler() {
      this.dialCardShow = false;
      // this.signalWebsocket.close();
      this.localMediaStreamOff();
      this.signalWebsocket.send(
        JSON.stringify({
          event: "end_call",
          dial_uuid: this.dialUUID,
        })
      );
      this.endCall();
    },
  },
};
</script>
<style>
.break-word {
  word-break: break-word;
}
.snackbar-content-class {
  display: flex;
  /* justify-content: space-between; */
  flex-direction: column;
}
.snackbar-content-btn-class {
  display: flex;
  justify-content: space-between;
}
.dial-card-posiotion {
  position: absolute !important;
  /* right: 10px;
  top: 70px; */
  z-index: 20;
}
.rotate-dial {
  transform: rotate(135deg);
}
.grey-background {
  background: grey;
}
</style>