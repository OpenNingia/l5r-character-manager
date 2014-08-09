import QtQuick 2.0

Rectangle {
    width: 600
    height: 200

    Row {
        id: row1
        x : 0
        y : 20
        width: 360
        height: 180

        Column {
            id: col1
            x: 12
            y: 12
            width: 128
            height: 170


            Image {
                id: img_portrait
                x: 0
                y: 0
                width: 128
                height: 128
                fillMode: Image.PreserveAspectFit
                source: "img/samurai.jpg"
            }
        }

        Column {
            id: col2
            x: 160
            y: 12
            width: 180
            height: 170

            TextEdit {
                id: tx_name
                x: 0
                y: 0
                width: 205
                height: 20
                text: qsTr("Hida Fudo")
                font.pointSize: 12
                font.pixelSize: 12
            }

            Text {
                id: tx_clan
                x: 0
                y: 24
                width: 205
                height: 20
                text: qsTr("Crab")
                font.pointSize: 12
                font.pixelSize: 12
            }

            Text {
                id: tx_family
                x: 0
                y: 44
                width: 205
                height: 20
                text: qsTr("Hida")
                font.pointSize: 12
                font.pixelSize: 12
            }

            Text {
                id: tx_school
                x: 0
                y: 64
                width: 205
                height: 20
                text: qsTr("Hida Bushi School")
                font.pointSize: 12
                font.pixelSize: 12
            }
        }

        Column
        {
            x: 260
            y: 0
            width: 180
            height: 170

            Image
            {
                id: img_logo_with_name
                x: 0
                y: 0
                opacity: 0.1
                //width: auto
                //height: auto
                source: "img/l5rlogowithname.png"
            }
        }
    }
 }

