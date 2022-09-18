<template>
  <div>
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
    <v-snackbar
      v-model="snackbarRejectInitCall"
      centered
      vertical
      timeout="3000"
      content-class="snackbar-content-class"
    >
      {{ snackbarRejectInitCallText }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="blue"
          text
          v-bind="attrs"
          @click="snackbarRejectInitCall = false"
        >
          Ok
        </v-btn>
      </template>
    </v-snackbar>

    <v-card
      v-bind:style="cardPosition"
      @mousedown="cardMouseDownHandle"
      @mouseup="cardMouseUpHandle"
      @mouseleave="cardMouseUpHandle"
      height="390"
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
      <video
        v-if="dialWithLocaleVideo"
        ref="refLocalVideo"
        width="150"
        height="150"
        autoplay
        muted
      ></video>
      <v-img
        v-else
        class="grey-background"
        height="150"
        contain
        :src="avatarSrc"
        ref="refLocalAvtr"
      ></v-img>
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
import { DIALS_ONLINE_TOOGLE } from "@/store/actions/user";

export default {
  name: "WebDial",
  props: {},
  data: function () {
    return {
      cardPosition: { left: "10px", top: "70px" },
      cardMove: false,
      opponentId: null,
      opponentType: null,
      dialCardShow: false,
      dialWithRemoteVideo: false,
      dialWithLocaleVideo: true,
      localVideo: true,
      signalWebsocket: null,
      mediaStreamLocal: null,
      mediaStreamRemote: null,
      pc: null,
      dialUUID: null,
      snackbarIncomeCall: false,
      snackbarIncomeCallText: "Вызов",
      snackbarRejectInitCall: false,
      snackbarRejectInitCallText: null,
      credentials: null,
      shiftPosCard: null,
    };
  },
  destroyed: async function () {
    this.signalWebsocket.close();
    await this.$store.dispatch(DIALS_ONLINE_TOOGLE, false);
  },
  mounted: async function () {
    this.setDialCardPosition();
    var vuel = this;
    this.$eventBus.$on(
      "initDial",
      ({ opponentId: opponentId, opponentType: opponentType }) => {
        vuel.opponentId = opponentId;
        vuel.opponentType = opponentType;
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

    dialElem.addEventListener("touchstart", vuel.cardMouseDownHandle);
    dialElem.addEventListener("touchend", vuel.cardMouseUpHandle);

    this.signalWebsocket = new WebSocket("wss://" + BASE_URL + "/ws/webdials/");
    this.signalWebsocket.onopen = async function () {
      await vuel.$store.dispatch(DIALS_ONLINE_TOOGLE, true);
    };
    this.signalWebsocket.onclose = async function () {
      vuel.localMediaStreamOff();
      await vuel.$store.dispatch(DIALS_ONLINE_TOOGLE, false);
    };
    this.signalWebsocket.onerror = async function () {
      vuel.localMediaStreamOff();
      await vuel.$store.dispatch(DIALS_ONLINE_TOOGLE, false);
    };

    this.signalWebsocket.onmessage = function (evt) {
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
        // console.log(offer);
        // инициирование локальных стримов при входящем звонке
        navigator.mediaDevices
          // запускаем видео и аудио
          .getUserMedia({ video: true, audio: true })
          .then((stream) => {
            vuel.mediaStreamLocal = stream;
            if (stream.getVideoTracks().length > 0) {
              vuel.$refs.refLocalVideo.srcObject = stream;
              vuel.dialWithLocaleVideo = true;
            } else {
              vuel.dialWithLocaleVideo = false;
            }
            if (offer.sdp.indexOf("video") != -1) {
              // video include
              vuel.dialWithRemoteVideo = true;
            } else {
              vuel.dialWithRemoteVideo = false;
            }
            stream
              .getTracks()
              .forEach((track) => vuel.pc.addTrack(track, stream));
            vuel.pc
              .setRemoteDescription(offer)
              .then(() => console.log("offer is set"))
              .catch(() => console.log("offer no good"));

            vuel.pc.createAnswer().then((answer) => {
              vuel.pc.setLocalDescription(answer);
              vuel.signalWebsocket.send(
                JSON.stringify({
                  event: "answer",
                  dial_uuid: msg.dial_uuid,
                  data: JSON.stringify(answer),
                })
              );
            });
          })
          .catch(() => {
            navigator.mediaDevices
              // запускаем аудио
              .getUserMedia({ audio: true })
              .then((stream) => {
                vuel.mediaStreamLocal = stream;
                if (stream.getVideoTracks().length > 0) {
                  vuel.$refs.refLocalVideo.srcObject = stream;
                  vuel.dialWithLocaleVideo = true;
                } else {
                  vuel.dialWithLocaleVideo = false;
                }
                if (offer.sdp.indexOf("video") != -1) {
                  // video include
                  vuel.dialWithRemoteVideo = true;
                } else {
                  vuel.dialWithRemoteVideo = false;
                }
                stream
                  .getTracks()
                  .forEach((track) => vuel.pc.addTrack(track, stream));
                vuel.pc
                  .setRemoteDescription(offer)
                  .then(() => console.log("offer is set"))
                  .catch(() => console.log("offer no good"));

                vuel.pc.createAnswer().then((answer) => {
                  vuel.pc.setLocalDescription(answer);
                  vuel.signalWebsocket.send(
                    JSON.stringify({
                      event: "answer",
                      dial_uuid: msg.dial_uuid,
                      data: JSON.stringify(answer),
                    })
                  );
                });
              })
              .catch(() => {
                window.alert("Нет доступа к камере и/или микрофону.");
              });
          });
      } else if (msg.event == "candidate") {
        let candidate = JSON.parse(msg.data);
        if (!candidate) {
          return console.log("failed to parse candidate");
        }
        vuel.pc
          .addIceCandidate(new RTCIceCandidate(candidate))
          .then(() => console.log("good candidate"))
          .catch(() => console.log("error candidate"));
      } else if (msg.event == "answer") {
        let answer = JSON.parse(msg.data);
        vuel.dialUUID = msg.dial_uuid;

        if (!answer) {
          return console.log("failed to parse answer");
        }
        if (answer.sdp.indexOf("video") != -1) {
          // video input include
          vuel.dialWithRemoteVideo = true;
        } else {
          vuel.dialWithRemoteVideo = false;
        }
        vuel.pc.setRemoteDescription(answer);
      } else if (msg.event == "init_call") {
        vuel.dialUUID = msg.dial_uuid;
        vuel.snackbarIncomeCallText = msg.init_call_username;
        vuel.snackbarIncomeCall = true;
      } else if (msg.event == "accept_init_call") {
        vuel.dialUUID = msg.dial_uuid;
        // init call
        vuel.initCall();
      } else if (msg.event == "reject_init_call") {
        // reject call
        vuel.dialUUID = null;
        vuel.emitInitCallEnd();
        if (msg.reason == "opponent_is_offline") {
          vuel.snackbarRejectInitCallText = "Пользователь не в сети.";
        } else if (msg.reason == "user_in_call") {
          vuel.snackbarRejectInitCallText =
            "Вы не можете инициировать второй вызов.";
        } else if (msg.reason == "opponent_is_busy") {
          vuel.snackbarRejectInitCallText = "Пользователь занят.";
        } else if (msg.reason == "opponent_reject") {
          vuel.snackbarRejectInitCallText = "Пользователь не принял вызов.";
        }
        vuel.snackbarRejectInitCall = true;
      } else if (msg.event == "end_call") {
        // vuel.dialUUID = null;
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
    setDialCardPosition() {
      if (localStorage.getItem("dialCardPositionLeft") != undefined) {
        this.cardPosition.left = localStorage.getItem("dialCardPositionLeft");
      }
      if (localStorage.getItem("dialCardPositionTop") != undefined) {
        this.cardPosition.top = localStorage.getItem("dialCardPositionTop");
      }
    },
    cardMouseDownHandle(event) {
      document.body.classList.add("lock-screen");
      this.cardMove = true;
      var elem = document.getElementById("dialCard");
      if (event.type == "mousedown") {
        this.shiftPosCard = {
          x: event.clientX - elem.getBoundingClientRect().left,
          y: event.clientY - elem.getBoundingClientRect().top,
        };
      } else if (event.type == "touchstart") {
        this.shiftPosCard = {
          x: event.touches[0].clientX - elem.getBoundingClientRect().left,
          y: event.touches[0].clientY - elem.getBoundingClientRect().top,
        };
      }
      // console.log(this.shiftPosCard);
      document.addEventListener("mousemove", this.moveCard);
      document.addEventListener("touchmove", this.moveCard);
    },
    cardMouseUpHandle() {
      document.body.classList.remove("lock-screen");
      this.cardMove = false;
      localStorage.setItem("dialCardPositionLeft", this.cardPosition.left);
      localStorage.setItem("dialCardPositionTop", this.cardPosition.top);
      document.removeEventListener("mousemove", this.moveCard);
      document.removeEventListener("touchmove", this.moveCard);
    },
    moveCard(event) {
      if (this.cardMove) {
        var elem = document.getElementById("dialCard");
        const width = elem.getBoundingClientRect().width;
        const height = elem.getBoundingClientRect().height;
        if (event.type == "mousemove") {
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
        } else if (event.type == "touchmove") {
          var t = event.touches[0];

          if (
            !(
              t.clientX - this.shiftPosCard.x < 10 ||
              t.clientX - this.shiftPosCard.x >
                document.documentElement.clientWidth - 10 - width
            )
          ) {
            this.cardPosition.left =
              (t.clientX - this.shiftPosCard.x).toString() + "px";
          }
          if (
            !(
              t.clientY - this.shiftPosCard.y < 70 ||
              t.clientY - this.shiftPosCard.y >
                document.documentElement.clientHeight - 10 - height
            )
          ) {
            this.cardPosition.top =
              (t.clientY - this.shiftPosCard.y).toString() + "px";
          }
        }
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
      var els = document.getElementsByClassName("remoteVideo");
      if (els.length) {
        document.querySelectorAll(".remoteVideo").forEach((el) => el.remove());
      }
    },
    localMediaStreamOff() {
      if (this.mediaStreamLocal != null) {
        this.mediaStreamLocal.getTracks().forEach(function (track) {
          track.stop();
        });
      }
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
        ],
      });

      this.pc.ontrack = function (event) {
        // добавление входящего стрима
        if (event.track.kind !== "audio" && event.track.kind !== "video") {
          return;
        }
        vuel.dialCardShow = true;
        vuel.dialWithRemoteVideo = event.track.kind === "video";
        let el = document.createElement(event.track.kind);
        el.srcObject = event.streams[0];
        el.autoplay = true;
        el.width = 150;
        el.height = 150;
        el.classList.add("remoteVideo");
        if (vuel.dialWithLocaleVideo) {
          vuel.$refs.refLocalVideo.before(el);
        } else {
          vuel.$refs.refLocalAvtr.$el.before(el);
        }
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
          this.emitInitCallEnd();
        }
      };
      this.pc.onicecandidate = (e) => {
        if (!e.candidate) {
          return;
        }
        vuel.signalWebsocket.send(
          JSON.stringify({
            event: "candidate",
            dial_uuid: vuel.dialUUID,
            data: JSON.stringify(e.candidate),
          })
        );
      };
    },
    emitInitCallEnd: function () {
      this.$eventBus.$emit("initDialEnd");
    },
    initCall() {
      var vuel = this;
      navigator.mediaDevices
        // пробуем запустить и видео, и аудио
        .getUserMedia({ video: true, audio: true })
        .then((stream) => {
          vuel.mediaStreamLocal = stream;
          if (stream.getVideoTracks().length > 0) {
            vuel.$refs.refLocalVideo.srcObject = stream;
            vuel.dialWithLocaleVideo = true;
          } else {
            vuel.dialWithLocaleVideo = false;
          }
          stream
            .getTracks()
            .forEach((track) => vuel.pc.addTrack(track, stream));

          vuel.pc.createOffer().then((offer) => {
            vuel.pc.setLocalDescription(offer);
            vuel.signalWebsocket.send(
              JSON.stringify({
                event: "offer",
                dial_uuid: vuel.dialUUID,
                data: JSON.stringify(offer),
              })
            );
          });
        })
        .catch(() => {
          navigator.mediaDevices
            // пробуем запустить аудио
            .getUserMedia({ audio: true })
            .then((stream) => {
              vuel.mediaStreamLocal = stream;
              if (stream.getVideoTracks().length > 0) {
                vuel.$refs.refLocalVideo.srcObject = stream;
                vuel.dialWithLocaleVideo = true;
              } else {
                vuel.dialWithLocaleVideo = false;
              }
              stream
                .getTracks()
                .forEach((track) => vuel.pc.addTrack(track, stream));

              vuel.pc.createOffer().then((offer) => {
                vuel.pc.setLocalDescription(offer);
                vuel.signalWebsocket.send(
                  JSON.stringify({
                    event: "offer",
                    dial_uuid: vuel.dialUUID,
                    data: JSON.stringify(offer),
                  })
                );
              });
            })
            .catch(() => {
              window.alert("Нет доступа к камере и/или микрофону.");
            });
        });
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
  position: fixed !important;
  /* right: 10px;
  top: 70px; */
  z-index: 7;
}
.rotate-dial {
  transform: rotate(135deg);
}
.grey-background {
  background: grey;
}
.lock-screen {
  height: 100%;
  overflow: hidden;
  width: 100%;
  position: fixed;
  overscroll-behavior: none;
}
</style>