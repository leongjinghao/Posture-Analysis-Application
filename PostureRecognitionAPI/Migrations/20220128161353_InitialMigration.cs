using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

namespace PostureRecognitionAPI.Migrations
{
    public partial class InitialMigration : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "DangerZoneCoordinates",
                columns: table => new
                {
                    id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    cameraId = table.Column<int>(type: "integer", nullable: false),
                    coordinates = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DangerZoneCoordinates", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "PostureLogs",
                columns: table => new
                {
                    id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    dateTime = table.Column<DateTime>(type: "timestamp without time zone", nullable: false),
                    cameraId = table.Column<int>(type: "integer", nullable: false),
                    zone = table.Column<string>(type: "text", nullable: true),
                    postureLandmarks = table.Column<string>(type: "text", nullable: true),
                    classification = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PostureLogs", x => x.id);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "DangerZoneCoordinates");

            migrationBuilder.DropTable(
                name: "PostureLogs");
        }
    }
}
