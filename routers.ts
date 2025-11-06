import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import { z } from "zod";
import {
  insertContinuumCycle,
  getLatestCycles,
  getCycleStats,
  insertConversationStarter,
  getConversationStarters,
  likeConversationStarter,
  insertVisualization,
  getVisualizations,
} from "./db";
import {
  ContinuumSimulator,
  getRandomConversationStarter,
  generateGalaxyData,
  generatePointCloudData,
  COSMIC_CONSTANTS,
} from "./continuum";

// Instance globale du simulateur
const simulator = new ContinuumSimulator();

export const appRouter = router({
  system: systemRouter,

  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  continuum: router({
    /**
     * Obtenir les constantes cosmiques
     */
    getConstants: publicProcedure.query(() => {
      return COSMIC_CONSTANTS;
    }),

    /**
     * Faire évoluer le Continuum d'un cycle
     */
    evolve: publicProcedure.mutation(async () => {
      const state = simulator.evolve();
      
      // Enregistrer dans la base de données
      await insertContinuumCycle({
        cycle: state.cycle,
        sectorId: state.sectorId,
        psi: state.psi,
        fusion: state.fusion,
        entropy: state.entropy,
        chaos: state.chaos,
        resonanceHz: state.resonanceHz,
        energyQ: state.energyQ,
        quantumEntanglement: state.quantumEntanglement,
        psiMagnitude: state.psiMagnitude,
      });

      return state;
    }),

    /**
     * Obtenir les derniers cycles
     */
    getLatestCycles: publicProcedure
      .input(z.object({ limit: z.number().optional() }))
      .query(async ({ input }) => {
        const cycles = await getLatestCycles(input.limit || 100);
        return cycles;
      }),

    /**
     * Obtenir les statistiques actuelles
     */
    getStats: publicProcedure.query(async () => {
      const stats = await getCycleStats();
      return stats;
    }),

    /**
     * Réinitialiser le simulateur
     */
    reset: publicProcedure.mutation(() => {
      simulator.reset();
      return { success: true };
    }),
  }),

  conversation: router({
    /**
     * Obtenir une amorce de conversation aléatoire
     */
    getRandom: publicProcedure.query(() => {
      return {
        question: getRandomConversationStarter(),
      };
    }),

    /**
     * Obtenir toutes les amorces de conversation
     */
    getAll: publicProcedure
      .input(z.object({ limit: z.number().optional() }))
      .query(async ({ input }) => {
        const starters = await getConversationStarters(input.limit || 50);
        return starters;
      }),

    /**
     * Créer une nouvelle amorce de conversation
     */
    create: protectedProcedure
      .input(
        z.object({
          question: z.string().min(10).max(500),
          category: z.string().optional(),
        })
      )
      .mutation(async ({ input, ctx }) => {
        await insertConversationStarter({
          userId: ctx.user.id,
          question: input.question,
          category: input.category || "general",
          isPublic: true,
        });

        return { success: true };
      }),

    /**
     * Liker une amorce de conversation
     */
    like: publicProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        const newLikes = await likeConversationStarter(input.id);
        return { likes: newLikes };
      }),
  }),

  visualization: router({
    /**
     * Générer des données de galaxie spirale
     */
    generateGalaxy: publicProcedure
      .input(z.object({ numPoints: z.number().optional() }))
      .query(({ input }) => {
        const data = generateGalaxyData(input.numPoints || 1000);
        return data;
      }),

    /**
     * Générer des données de nuage de points
     */
    generatePointCloud: publicProcedure
      .input(z.object({ numPoints: z.number().optional() }))
      .query(({ input }) => {
        const data = generatePointCloudData(input.numPoints || 500);
        return data;
      }),

    /**
     * Sauvegarder une visualisation
     */
    save: protectedProcedure
      .input(
        z.object({
          type: z.enum(["galaxy", "pointcloud", "fractal"]),
          cycle: z.number(),
          dataUrl: z.string().optional(),
          thumbnailUrl: z.string().optional(),
          metadata: z.string().optional(),
        })
      )
      .mutation(async ({ input, ctx }) => {
        await insertVisualization({
          userId: ctx.user.id,
          type: input.type,
          cycle: input.cycle,
          dataUrl: input.dataUrl || null,
          thumbnailUrl: input.thumbnailUrl || null,
          metadata: input.metadata || null,
        });

        return { success: true };
      }),

    /**
     * Obtenir les visualisations
     */
    getAll: publicProcedure
      .input(
        z.object({
          userId: z.string().optional(),
          limit: z.number().optional(),
        })
      )
      .query(async ({ input }) => {
        const visualizations = await getVisualizations(
          input.userId,
          input.limit || 50
        );
        return visualizations;
      }),
  }),
});

export type AppRouter = typeof appRouter;

