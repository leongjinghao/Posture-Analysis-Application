using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Data;
using PostureRecognitionAPI.Models;
using System.IO;
using System.Reflection;

namespace PostureRecognitionAPI.Repositories
{
    public class PostureVideoPathRepository : IPostureVideoPathRepository
    {
        private readonly IDataContext _context;
        public PostureVideoPathRepository(IDataContext context)
        {
            _context = context;

        }

        // Add new record in PostureVideoPaths table using a postureVideoPath object
        public async Task Add(PostureVideoPath postureVideoPath)
        {
            /* line 27 to 38: set upper limit for video recording stored to 20
               Delete this section when upper limit not required */
            // retrieve existing number of video recordings stored
            var allVideoRecordings = await _context.PostureVideoPaths.Select(pvp => pvp.postureVideoPath).ToListAsync();
            var videoCount = allVideoRecordings.Count();
            
            // if there are already 20 video recordings stored, 
            // delete earliest video recording stored before adding
            if (videoCount == 20) {
                // extract first (earliest) video name from path retrieved as the input for Delete() function 
                var videoName = allVideoRecordings[0].Replace("posture_video_recording/", "");
                // delete the earliest video recording stored
                Task task = Delete(videoName);
            }

            // add the new video recording's path
            _context.PostureVideoPaths.Add(postureVideoPath);
            await _context.SaveChangesAsync();
        }

        // Delete the specified record in PostureVideoPaths table with a given video name
        public async Task Delete(string videoName)
        {
            // Check if the provided video name exist
            var itemToDelete = await (_context.PostureVideoPaths.Where(vp => vp.postureVideoPath.Contains(videoName))).FirstAsync();
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            // Delete record from table
            _context.PostureVideoPaths.Remove(itemToDelete);
            await _context.SaveChangesAsync();

            // retrieve directory of root dir
            string path = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string repoPath = Directory.GetParent(
                                Directory.GetParent(
                                    Directory.GetParent(
                                        Directory.GetParent(path).FullName).FullName).FullName).FullName;
            string reactPublicPath = repoPath + "\\my-app\\public\\posture_video_recording";
            string fullVideoPath = reactPublicPath + "\\" + videoName;

            // delete video recording stored in React public folder
            File.Delete(@fullVideoPath);
        }

        // Get the postureVideoPath attributes with a given id
        public async Task<PostureVideoPath> Get(int id)
        {
            return await _context.PostureVideoPaths.FindAsync(id);
        }

        // Get all the postureVideoPath attributes
        public async Task<IEnumerable<PostureVideoPath>> GetAll()
        {
            return await _context.PostureVideoPaths.ToListAsync();
        }

        // Update the specified record in PostureVideoPaths table with a given postureVideoPath object
        public async Task Update(PostureVideoPath postureVideoPath)
        {
            // Check if the id of provided postureVideoPath object exist
            var itemToUpdate = await _context.PostureVideoPaths.FindAsync(postureVideoPath.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            // Update record of the id tied with the given postureVideoPath object
            itemToUpdate.postureVideoPath = postureVideoPath.postureVideoPath;
            await _context.SaveChangesAsync();
        }
    }
}