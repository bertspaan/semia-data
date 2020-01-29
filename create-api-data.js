#!/usr/bin/env node

const fs = require('fs')
const path = require('path')
const H = require('highland')

function jsonStream (filename) {
  return H(fs.createReadStream(filename))
    .split()
    .compact()
    .map(JSON.parse)
}

function getShotLengths () {
  return new Promise((resolve, reject) => {
    jsonStream(path.join(__dirname, 'source/shot-lengths/shot-lengths.ndjson'))
      .group('vid_id')
      .toArray((groups) => resolve(groups[0]))
  })
}

function getClosestShots () {
  return new Promise((resolve, reject) => {
    return jsonStream(path.join(__dirname, 'source/similar-shots/similar-shots.ndjson'))
      .group('shot_id')
      .toArray((groups) => resolve(groups[0]))
  })
}
const numClosestShots = 5
function sliceSimilar (closestShotsForShot, variable) {
  return closestShotsForShot.results[variable]
    .slice(0, numClosestShots)
    .map((shotId) => {
      const [videoId, shotIndex] = shotId.split('_')
      return [parseInt(videoId), parseInt(shotIndex)]
    })
}

(async () => {
  const shotLengths = await getShotLengths()
  const closestShots = await getClosestShots()

  jsonStream(path.join(__dirname, 'source/metadata/metadata.ndjson'))
    .filter((video) => video.attributionURL && video.attributionURL[0])
    .map((video) => {
      const videoId = path.basename(video.attributionURL[0])
      const shots = shotLengths[videoId]

      if (!shots) {
        console.error(`No shots found for video ${videoId}`)
        return
      }

      const title = video.title[0]
      const date = video.date[0]
      const description = video.description[0]
      const abstract = video.abstract[0]
      const url = video.attributionURL[0]

      const length = shots[shots.length - 1].end

      return {
        id: parseInt(videoId),
        title,
        date,
        description,
        abstract,
        url,
        medium: video.medium,
        length,
        shots: shots.map((shot) => {
          const shotId = shot.shot_id

          const closestShotsForShot = closestShots[shotId][0]

          let similar
          if (!closestShotsForShot) {
            console.error(`No closest shots found for video ${videoId}`)
          } else {
            similar = {
              colour: sliceSimilar(closestShotsForShot, 'colour'),
              shape: sliceSimilar(closestShotsForShot, 'shape'),
              movement: sliceSimilar(closestShotsForShot, 'movement'),
              clutter: sliceSimilar(closestShotsForShot, 'clutter')
            }
          }

          return {
            start: shot.start,
            end: shot.end,
            similar
          }
        })
      }
    })
    .compact()
    .map(JSON.stringify)
    .intersperse('\n')
    .pipe(process.stdout)
})()
