<template>
    <section>
        <div class="card-body">
            <div class="messages">
                <p><span class="font-weight-bold">{{ message }} </span></p>
            </div>
        </div>
        <span class="is-centered" v-if=" finished  === true">
                    <a href="url"> {{link}}}</a>
            <!--<button class="button" style="margin-right: 12.25px" @click="">Download</button>-->

        </span>
    </section>
</template>


<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                dropFiles: [],
                uploaded: false,
                uuid:'DEFAULT UUID',
                status:'',
                isConnected: false,
                message:'DEFAULT MESSAGE',
                messages:[],
                socket : null,
                finished: false,
                downloadLink: '',

            }
        },
        methods: {
            createWebSocket(uuid) {
                const ws = new WebSocket("ws://localhost:5555/progress/socket?uuid="+uuid)
                ws.onopen = function() {
                    // ws.send("Ready to start");
                    console.log("connecting to socket")
                };
                ws.onmessage = (evt) => {
                    // console.log(evt.data)
                    // console.log(this.message)
                    this.message = evt.data
                };
                this.socket = ws
            }
        },
        watch: {
            message(){
                // console.log(this.message)
                if (this.message === 'file is ready to download') {
                    this.finished = true
                    this.downloadLink = 'localhost:5555/download?uuid='+this.uuid
                }
            }
        },
        mounted() {
            if(this.socket) {
                console.log("hello from mounted")
                this.socket.onmessage = function (evt) {
                    this.message = evt.data
                };
            }
            else {
                this.createWebSocket(this.uuid)
            }
            // this.socket.on('MESSAGE', (data) => {
            //     this.message = data;
            //     console.log(data)
            // });
            // this.socket.on('FINISH', (data) => {
            //     this.finished = data;
            //     console.log(data)
            // });
            // }
        }
    }
</script>

<!--<style scoped>-->

<!--</style>-->