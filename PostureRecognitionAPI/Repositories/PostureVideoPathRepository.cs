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
        public async Task Add(PostureVideoPath postureVideoPath)
        {
            _context.PostureVideoPaths.Add(postureVideoPath);
            await _context.SaveChangesAsync();
        }

        public async Task Delete(string videoName)
        {
            // delete posture video path stored in database table
            var itemToDelete = await (_context.PostureVideoPaths.Where(vp => vp.postureVideoPath.Contains(videoName))).FirstAsync();
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            _context.PostureVideoPaths.Remove(itemToDelete);
            await _context.SaveChangesAsync();

            // delete video recording stored in React public folder
            // retrieve directory of root dir
            string path = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string repoPath = Directory.GetParent(
                                Directory.GetParent(
                                    Directory.GetParent(
                                        Directory.GetParent(path).FullName).FullName).FullName).FullName;
            string reactPublicPath = repoPath + "\\my-app\\public\\posture_video_recording";
            string fullVideoPath = reactPublicPath + "\\" + videoName;

            File.Delete(@fullVideoPath);
        }

        public async Task<PostureVideoPath> Get(int id)
        {
            return await _context.PostureVideoPaths.FindAsync(id);
        }

        public async Task<IEnumerable<PostureVideoPath>> GetAll()
        {
            return await _context.PostureVideoPaths.ToListAsync();
        }

        public async Task Update(PostureVideoPath postureVideoPath)
        {
            var itemToUpdate = await _context.PostureVideoPaths.FindAsync(postureVideoPath.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.postureVideoPath = postureVideoPath.postureVideoPath;
            await _context.SaveChangesAsync();
        }
    }
}